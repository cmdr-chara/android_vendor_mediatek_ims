#!/usr/bin/env python3
"""GNU Make product-scope contracts; not an Android build or carrier test."""
import os
from pathlib import Path
import shutil
import subprocess
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def evaluate(local_path):
    source = Path(os.environ.get('IMS_MAKEFILE', ROOT / 'ims.mk')).resolve()
    makefile = f'''LOCAL_PATH := {local_path}
TARGET_COPY_OUT_SYSTEM := system
TARGET_COPY_OUT_VENDOR := vendor
include {source}
$(info LOCAL_PATH=$(LOCAL_PATH))
$(info PACKAGES=$(strip $(PRODUCT_PACKAGES)))
$(info NAMESPACES=$(strip $(PRODUCT_SOONG_NAMESPACES)))
$(info PROPERTIES=$(strip $(PRODUCT_PRODUCT_PROPERTIES)))
$(info COPIES=$(strip $(PRODUCT_COPY_FILES)))
.PHONY: all
all: ; @:
'''
    result = subprocess.run(['make', '-s', '--no-print-directory', '-f', '-', 'all'],
                            input=makefile, text=True, capture_output=True, check=True, timeout=10)
    return dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)


class ProductScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if shutil.which('make') is None:
            raise RuntimeError('GNU Make is required')

    def test_caller_local_path_is_preserved(self):
        for caller in ('device/xiaomi/malachite', 'device/example/other', ''):
            with self.subTest(caller=caller):
                self.assertEqual(evaluate(caller)['LOCAL_PATH'], caller)

    def test_package_property_and_namespace_contract_is_unchanged(self):
        result = evaluate('device/xiaomi/malachite')
        self.assertEqual(result['PACKAGES'].split(), ['ImsService', 'mtk-ims', 'mtk-ims-telephony'])
        self.assertEqual(result['NAMESPACES'], 'vendor/mediatek/ims')
        self.assertEqual(result['PROPERTIES'].split(), [
            'persist.dbg.volte_avail_ovr=1', 'persist.dbg.vt_avail_ovr=1',
            'persist.dbg.wfc_avail_ovr=1', 'persist.vendor.vilte_support=0',
            'persist.vendor.ims_support=1', 'persist.vendor.volte_support=1'])

    def test_exact_copy_sources_destinations_and_local_xml(self):
        copies = evaluate('device/xiaomi/malachite')['COPIES'].split()
        self.assertEqual(copies, [
            'vendor/mediatek/ims/configs/permissions/privapp-permissions-com.mediatek.ims.xml:system/etc/permissions/privapp-permissions-com.mediatek.ims.xml',
            'vendor/mediatek/ims/configs/sysconfig/com.mediatek.ims.config.xml:system/etc/sysconfig/com.mediatek.ims.config.xml',
            'frameworks/native/data/etc/android.hardware.telephony.ims.xml:vendor/etc/permissions/android.hardware.telephony.ims.xml'])
        for copy in copies[:2]:
            source = copy.split(':')[0].removeprefix('vendor/mediatek/ims/')
            ET.parse(ROOT / source)


if __name__ == '__main__':
    unittest.main()
