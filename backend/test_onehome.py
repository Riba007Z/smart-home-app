from onehome import get_devices

devices = get_devices()

print("=== Devices ===")

for d in devices:
    print(
        d["name"],
        d["groupAddress"],
        d["dptType"]
    )