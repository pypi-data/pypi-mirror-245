/*!
 * Licensed under the MIT license.
 * See LICENSE file in the project root for full license information.
 * Created by Junjie Gao on 2023/3/1.
 */

#ifndef UTBOOST_INCLUDE_UTBOOST_UTILS_LOG_WRAPPER_H_
#define UTBOOST_INCLUDE_UTBOOST_UTILS_LOG_WRAPPER_H_

#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <exception>
#include <iostream>
#include <stdexcept>
#include <string>

namespace UTBoost {

#ifndef ASSERT
#define ASSERT(condition)                                                   \
  if (!(condition))                                                         \
    Log::Error("Assert error: " #condition " at %s, line %d .\n", __FILE__, __LINE__);
#endif

#ifndef ASSERT_NOTNULL
#define ASSERT_NOTNULL(pointer)                                        \
  if ((pointer) == nullptr)                                            \
    Log::Error("Assert error: " #pointer " can't be NULL at %s, line %d .\n",  __FILE__, __LINE__);
#endif

#ifndef ASSERT_EQ
#define ASSERT_EQ(a, b) ASSERT((a) == (b))
#endif

#ifndef ASSERT_NE
#define ASSERT_NE(a, b) ASSERT((a) != (b))
#endif

#ifndef ASSERT_GE
#define ASSERT_GE(a, b) ASSERT((a) >= (b))
#endif

#ifndef ASSERT_LE
#define ASSERT_LE(a, b) ASSERT((a) <= (b))
#endif

#ifndef ASSERT_GT
#define ASSERT_GT(a, b) ASSERT((a) > (b))
#endif

#ifndef ASSERT_LT
#define ASSERT_LT(a, b) ASSERT((a) < (b))
#endif

enum class LogLevel : int {
  Fatal = -1,
  Warning = 0,
  Info = 1,
  Debug = 2,
};

/*!
 * \brief A static Log class
 */
class Log {
 public:
  using Callback = void (*)(const char *);
  /*!
   * \brief Resets the minimal log level. It is INFO by default.
   * \param level The new minimal log level.
   */
  static void ResetLogLevel(LogLevel level) { GetLevel() = level; }

  /*! \brief Whether to filter debugging information. */
  static void Verbose() { ResetLogLevel(LogLevel::Debug); }

  static void ResetCallBack(Callback callback) { GetLogCallBack() = callback; }

  static void Debug(const char *format, ...) {
    va_list val;
    va_start(val, format);
    Write(LogLevel::Debug, "Debug", format, val);
    va_end(val);
  }
  static void Info(const char *format, ...) {
    va_list val;
    va_start(val, format);
    Write(LogLevel::Info, "Info", format, val);
    va_end(val);
  }
  static void Warn(const char *format, ...) {
    va_list val;
    va_start(val, format);
    Write(LogLevel::Warning, "Warn", format, val);
    va_end(val);
  }
  static void Error(const char *format, ...) {
    va_list val;
    const size_t kBufSize = 1024;
    char str_buf[kBufSize];
    va_start(val, format);
#ifdef _MSC_VER
    vsnprintf_s(str_buf, kBufSize, format, val);
#else
    vsnprintf(str_buf, kBufSize, format, val);
#endif
    va_end(val);
    fprintf(stderr, "[UTBoost] [Error] %s\n", str_buf);
    fflush(stderr);
    throw std::runtime_error(std::string(str_buf));
  }

 private:
  static void Write(LogLevel level, const char *level_str, const char *format,
                    va_list val) {
    if (level <= GetLevel()) {  // omit the message with low level
      if (GetLogCallBack() == nullptr) {
        printf("[UTBoost] [%s] ", level_str);
        vprintf(format, val);
        printf("\n");
        fflush(stdout);
      } else {
        const size_t kBufSize = 512;
        char buf[kBufSize];
        snprintf(buf, kBufSize, "[UTBoost] [%s] ", level_str);
        GetLogCallBack()(buf);
        vsnprintf(buf, kBufSize, format, val);
        GetLogCallBack()(buf);
        GetLogCallBack()("\n");
      }
    }
  }

#if defined(_MSC_VER)
  static LogLevel& GetLevel() { static __declspec(thread) LogLevel level = LogLevel::Info; return level; }
#else
  static LogLevel& GetLevel() { static thread_local LogLevel level = LogLevel::Info; return level; }
#endif

  static Callback &GetLogCallBack() {
    static thread_local Callback callback = nullptr;
    return callback;
  }
};

}


#endif //UTBOOST_INCLUDE_UTBOOST_UTILS_LOG_WRAPPER_H_
