#ifndef __ROS_EXCEPTIONS_HXX__
#define __ROS_EXCEPTIONS_HXX__

#include <exception>

namespace RailOSTools {
class parsing_error : public std::exception {
private:
  const char* message_;
public:
  parsing_error(const char* msg): message_(msg) {}
  const char* what() const throw() {
    return message_;
  }
};
};

#endif
