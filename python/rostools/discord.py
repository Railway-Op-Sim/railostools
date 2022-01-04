import glob
import os.path
import asyncio
import logging
import datetime

import toml
import pycountry
import configparser

import discordsdk

from rostools.common import Level1Mode, Level2OperMode


def alpha2_country_codes():
    return {
        country.alpha_2: country.name.lower().replace(' ', '-')
        for country in pycountry.countries
    }


class DiscordBroadcaster:
    _version = 'v0.1.0-alpha'
    _logger = logging.getLogger('ROSTools.Discord')
    _activity = discordsdk.Activity()
    _logo_key = "railway_operation_simulator_logo"
    _flags = alpha2_country_codes()
    _oper_mode_statuses = {
        Level2OperMode.NoOperMode: '',
        Level2OperMode.Paused: 'Paused',
        Level2OperMode.Operating: 'Operating',
        Level2OperMode.PreStart: 'Loading'
    }
    _welcome_message = '''
=============================================================================

                Railway Operation Simulator Discord Launcher 
                                {version}
                                
                            _____╔°_________
                                   ╱                           
                            ______╱__°╗_____
                            
    This executable updates your user Discord status during an ROS session!
    
============================================================================= 
'''

    def __init__(self, ros_location: str, discord_app_id_file: str) -> None:
        if not os.path.exists(ros_location):
            raise FileNotFoundError(
                f"Cannot location Railway Operation Simulator, path '{ros_location}' "
                "does not exist"
            )
        if not os.path.exists(discord_app_id_file):
            raise FileNotFoundError(
                f"Cannot open application ID file, '{discord_app_id_file}' does not exist"
            )
        self._logger.info(self._welcome_message.format(version=self._version))
        self._start = datetime.datetime.now()
        self._running = True
        self._mode = {'main': '', 'oper': ''}
        self._ros_loc = ros_location
        self._discord = discordsdk.Discord(int(open(discord_app_id_file).read()), discordsdk.CreateFlags.default)
        self._discord.get_user_manager().on_current_user_update = self.on_curr_user_update
        self._activity.assets.large_image = self._logo_key
        self._activity.assets.large_text = "Testing"
        self._activity.details = ""
        self._activity.state = ""

    def on_curr_user_update(self) -> None:
        user = self._discord.get_user_manager().get_current_user()
        self._logger.info(f"Updating activity for user : {user.username}#{user.discriminator}")

    def activity_callback(self, result) -> None:
        if result == discordsdk.Result.ok:
            self._logger.info("Activity set successfully!")
        else:
            raise Exception(result)

    async def _run_sdk(self) -> None:
        while self._running:
            await asyncio.sleep(1 / 10.)
            self._discord.run_callbacks()

    def _check_for_metadata(self, route: str):
        if not os.path.exists(os.path.join(self._ros_loc, 'Metadata')):
            return {}

        _meta_list = [
            os.path.splitext(os.path.basename(i))[0]
            for i in glob.glob(os.path.join(self._ros_loc, 'Metadata', '*.toml'))
        ]

        if os.path.splitext(os.path.basename(route))[0] not in _meta_list:
            return {}

        _data = toml.load(
            os.path.join(self._ros_loc, 'Metadata', f'{os.path.splitext(os.path.basename(route))[0]}.toml'))

        if 'rly_file' not in _data or os.path.splitext(_data['rly_file'])[
            0
        ] != os.path.basename(route):
            return {}

        return _data

    def _load_session_ini(self) -> configparser.ConfigParser:
        _session_data = os.path.join(self._ros_loc, 'session.ini')

        if not os.path.exists(_session_data):
            raise FileNotFoundError(
                f"Expected session metadata file '{_session_data}', but file does not exist"
            )

        _parser = configparser.ConfigParser()
        _parser.read(_session_data)

        return _parser

    def _update_status(self, parser: configparser.ConfigParser):
        try:
            _top_mode = Level1Mode(parser.getint('session', 'main_mode'))
            _oper_mode = Level2OperMode(parser.getint('session', 'operation_mode'))
        except configparser.NoOptionError:
            return

        if self._mode['main'] == _top_mode and self._mode['oper'] == _oper_mode:
            return

        self._mode['main'] = _top_mode
        self._mode['oper'] = _oper_mode

        _activity = ''
        _new_status = ''

        if _top_mode == Level1Mode.OperMode:
            _activity = self._oper_mode_statuses[_oper_mode]
            self._activity.timestamps.start = datetime.datetime.timestamp(datetime.datetime.now())
        else:
            if _top_mode == Level1Mode.TrackMode:
                _activity = 'Editing'
            else:
                _activity = ''
                _new_status = ''
            self._activity.timestamps.start = 0

        if _activity:
            try:
                _current_rly = parser.get('session', 'railway')
                _meta = self._check_for_metadata(_current_rly)
                _current_rly = _current_rly.replace('_', ' ').title()
                if _meta and 'country_code' in _meta:
                    self._logger.info(f"Recognised country code '{_meta['country_code']}'")
                    try:
                        self._activity.assets.small_image = self._flags[_meta['country_code']]
                    except KeyError:
                        self._logger.debug("No country found for simulation, no sub-icon will be used")
                _new_status = f"{_activity} {_current_rly}"
            except configparser.NoOptionError:
                self._logger.error("Failed to find key 'railway' in INI file")

        if self._activity.details != _new_status and _new_status:
            self._activity.details = _new_status
            self._discord.get_activity_manager().update_activity(self._activity, self.activity_callback)

    async def _check_for_temp(self) -> None:
        while self._running:
            await asyncio.sleep(2)
            _parser = self._load_session_ini()
            self._running = _parser.getboolean('session', 'running')
            self._update_status(_parser)

    async def _run_ros(self) -> None:
        if not os.path.exists(os.path.join(self._ros_loc, 'railway.exe')):
            raise FileNotFoundError(
                f"No binary '{os.path.join(self._ros_loc, 'railway.exe')}' was found"
            )
        await asyncio.create_subprocess_shell(os.path.join(self._ros_loc, 'railway.exe'))

    async def _main(self):
        await asyncio.gather(self._run_sdk(), self._check_for_temp(), self._run_ros())

    def run(self):
        self._start = datetime.datetime.now()
        self._discord.get_activity_manager().update_activity(self._activity, self.activity_callback)
        asyncio.run(self._main())


if __name__ in "__main__":
    logging.getLogger('ROSTools').setLevel(logging.DEBUG)
    DiscordBroadcaster(
        '..',
        os.path.join(os.path.dirname(__file__),
                     os.path.join(os.getcwd(), 'discord_app_id.txt'))
    ).run()
