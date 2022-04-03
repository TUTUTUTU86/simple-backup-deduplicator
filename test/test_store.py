from src.dd.store.manifest_store import ManifestStore
from src.dd.store.manifest_store import Manifest


def test_manifest_store():
    manifest_store = ManifestStore("test.store")
    manifest = Manifest()
    for i in range(100):
        manifest.hash_list.append(i)
    manifest_store.save(manifest)
    loaded_manifest = manifest_store.load(0)
    print(loaded_manifest.hash_list)

