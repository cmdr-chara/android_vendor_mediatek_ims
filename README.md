# MediaTek IMS for the malachite revival

This owned fork supplies the prebuilt `ImsService` APK, two runtime resource overlays, permissions, sysconfig and the product fragment `ims.mk`. The initial source baseline is `lineage-23.2` at `06c462f1dfc2bb62e70e1d827b14bb364dc97857`. This is a source-revision record, not certification of carrier registration or Android-version compatibility.

## Integration

Use the project's pinned Android local manifest where available. For a standalone source checkout:

```sh
git clone --branch lineage-23.2 https://github.com/cmdr-chara/android_vendor_mediatek_ims vendor/mediatek/ims
```

A branch moves. Record the reviewed commit in the coordinated workspace lock and capture `repo manifest -r` for each build. Review candidates may be on `revival/*` branches until their PRs are integrated.

In the device product:

```make
$(call inherit-product, vendor/mediatek/ims/ims.mk)
```

The fragment uses `MTK_IMS_PATH` for its own resources and must not overwrite the caller's `LOCAL_PATH`. Package names, feature properties and copy destinations remain compatible with the inspected baseline.

## Compatibility and provenance gates

`Android.bp` and `Android.mk` define the actual APK installation/signing behavior. The checked-in APK is a prebuilt; this repository is not evidence of a reproducible rebuild of all proprietary IMS components. Its latest baseline update refers to the patched IMS work in [Nothing-2A/android_device_nothing_Aerodactyl](https://github.com/Nothing-2A/android_device_nothing_Aerodactyl/commit/4abe46a3867bf3214ab39abac23630ef8c84e124). Preserve that history and establish source/APK hashes and signature provenance before replacing it.

The package does not remove the device's dependency on a compatible radio HAL, modem firmware, vendor userspace, permissions and carrier provisioning. Feature-availability properties in `ims.mk` are not proof that VoLTE or VoWiFi registered. No blanket claim is made for Android 16 or every newer version, every VNDK-S-or-newer vendor, or every carrier.

For malachite, keep the coordinated vendor/userspace baseline. Do not replace camera/vendor blobs with OS3 merely because the reported fingerprint is newer. Do not downgrade or cross-flash regional modem/bootloader firmware to make IMS work.

## Checks

```sh
python3 -m unittest discover -s tests -p 'test_product_scope.py' -v
```

These offline GNU Make tests check caller scope, exact package/property/namespace/copy contracts and local XML well-formedness. They are not Kati/Soong, APK-signature, merged-VINTF or device tests.

Before release, validate the APK and privileges in the actual Android build, radio/VINTF compatibility, then separately authorized on-device SIM registration, voice/SMS/data, VoLTE, VoWiFi and handover for the actual carrier/SKU. Emergency-call behavior needs a suitable authorized test arrangement; do not place unsolicited emergency calls. Collect logs without publishing subscriber identifiers or credentials.

## Attribution and licensing

This fork retains the upstream history and attribution, including the original work associated with [techyminati/android_vendor_mediatek_ims](https://github.com/techyminati/android_vendor_mediatek_ims). See `LICENSE` and per-file notices. Fork ownership does not change the provenance or licensing obligations of proprietary prebuilts.
