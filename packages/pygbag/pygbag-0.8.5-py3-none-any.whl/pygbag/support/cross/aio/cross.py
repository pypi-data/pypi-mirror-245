import sys

DEBUG = False

import aio.prepro

aio.prepro.DEBUG = DEBUG

#
platform_impl = False

# ================== leverage known python implementations ====================

# always come down to upy choices because cpython syntax can more easily be adapted


if not defined("__UPY__"):
    define("__UPY__", hasattr(sys.implementation, "_mpy"))

    if not __UPY__:
        # setup exception display with same syntax as upy
        import traceback

        def print_exception(e, out=sys.stderr, **kw):
            kw["file"] = out
            traceback.print_exc(**kw)

        sys.print_exception = print_exception
        del print_exception


if not defined("__WASM__"):
    try:
        # that sym cannot be overloaded in the simulator
        if __import__("os").uname().machine.startswith("wasm"):
            import __WASM__
        else:
            __WASM__ = False
    except AttributeError:
        # upy does not have os.uname
        __WASM__ = True

    define("__WASM__", __WASM__)


if not defined("__wasi__"):
    if sys.platform == "wasi":
        import __wasi__
    else:
        __wasi__ = False

define("__wasi__", __wasi__)


# this *is* the cpython way
if hasattr(sys, "getandroidapilevel"):
    platform_impl = defined("__ANDROID__")
    if not platform_impl:
        print("importing platform_impl __ANDROID__")
        try:
            import __ANDROID__ as platform_impl
        except Exception as e:
            if hasattr(sys, "print_exception"):
                sys.print_exception(e)
            else:
                __import__("traceback").print_exc()

            pdb("__ANDROID__ failed to load, assuming simulator instead of error :")
            del platform_impl

            # fake it
            platform_impl == __import__("__main__")
        define("__ANDROID__", platform_impl)
    try:
        __ANDROID_API__
    except:
        defined("__ANDROID_API__", sys.getandroidapilevel())

define("__ANDROID__", platform_impl)


if sys.platform == "emscripten":
    platform_impl = defined("__EMSCRIPTEN__")
    if not platform_impl:
        try:
            import __EMSCRIPTEN__ as platform_impl
        except Exception as e:
            if hasattr(sys, "print_exception"):
                sys.print_exception(e)
            else:
                __import__("traceback").print_exc()

            pdb("__EMSCRIPTEN__ failed to load, assuming simulator instead of error :")
            del platform_impl

            # fake it
            platform_impl == __import__("__main__")

define("__EMSCRIPTEN__", platform_impl)


driver = defined("embed")
try:
    if not driver:
        import embed as driver
except:
    # else use the simulator defined platform_impl value as the embed.
    driver = platform_impl
if driver:
    # just in case it was not a module
    sys.modules.setdefault("embed", driver)

    try:
        # check it the embedding module was finished for that platform_impl.
        # the least shoulbe syslog ( js console / adb logcat )
        driver.log
    except:
        pdb(
            """\
    WARNING: embed softrt/syslog functions not found
    WARNING: also not in __main__ or simulator provided platform_impl module
    """
        )
        driver.enable_irq = print
        driver.disable_irq = print
        driver.log = print

    define("embed", driver)

    platform_impl.init_platform(driver)
    sys.modules["platform"] = platform_impl


if not __UPY__:
    # setup exception display with same syntax as upy
    import traceback

    def print_exception(e, out=sys.stderr, **kw):
        kw["file"] = out
        traceback.print_exc(**kw)

    sys.print_exception = print_exception
    del print_exception


scheduler = None
simulator = None
