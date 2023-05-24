import pkgutil

package = "gaze_tracking"
installed = pkgutil.find_loader(package) is not None

if installed:
    print(f"{package} is installed.")
else:
    print(f"{package} is not installed.")



