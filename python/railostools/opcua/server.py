import opcua
import time
import opcua.ua

import railostools.session as ros_sesh

class RailOSMetaServer:
    _server = opcua.Server()
    _variables = {
        "session": {
            "timetable": ("", opcua.ua.VariantType.String),
            "railway": ("", opcua.ua.VariantType.String),
        }
    }
    def __init__(self, railway_op_sim_dir: str, port: int = 4080) -> None:
        self._server.set_endpoint(f"opc.tcp://127.0.0.1:{port}")
        self._session = ros_sesh.Session(railway_op_sim_dir)
        self._namespace = self._server.register_namespace("RailOS")
        self._node = self._server.get_objects_node()
        self._vars = self._register_parameter_sets()

    def _register_parameter_sets(self) -> None:
        _vars = {k: {} for k in self._variables}
        for name, param_set in self._variables.items():
            _set = self._node.add_object(
                self._namespace,
                f"{name}_parameters"
            )
            for key, value in param_set.items():
                _new_var = _set.add_variable(
                    self._namespace,
                    key, *value
                )
                _new_var.set_writable()
                _vars[name][key] = _new_var
        return _vars

    def update(self) -> None:
        for key in self._vars["session"]:
            self._vars["session"][key].set_value(getattr(self._session, key) or "")

    def __enter__(self) -> None:
        self._server.start()
        while True:
            time.sleep(1)
            try:
                self.update()
            except:
                continue

    def __exit__(self, *args, **kwargs) -> None:
        self._server.stop()


if __name__ in "__main__":
    with RailOSMetaServer("C:/Program Files/RailwayOperationSimulator/Railway") as server:
        pass