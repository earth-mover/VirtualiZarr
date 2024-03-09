import pytest

from virtualizarr.manifest import ChunkManifest


class TestCreateManifest:
    def test_create_manifest(self):
        chunks = {
            "0.0.0": {"path": "s3://bucket/foo.nc", "offset": 100, "length": 100},
        }
        manifest = ChunkManifest(chunkentries=chunks)
        assert manifest.chunks == chunks

        chunks = {
            "0.0.0": {"path": "s3://bucket/foo.nc", "offset": 100, "length": 100},
            "0.0.1": {"path": "s3://bucket/foo.nc", "offset": 200, "length": 100},
            "0.1.0": {"path": "s3://bucket/foo.nc", "offset": 300, "length": 100},
            "0.1.1": {"path": "s3://bucket/foo.nc", "offset": 400, "length": 100},
        }
        manifest = ChunkManifest(chunkentries=chunks)
        assert manifest.chunks == chunks

    def test_invalid_chunk_entries(self):
        chunks = {
            "0.0.0": {"path": "s3://bucket/foo.nc"},
        }
        with pytest.raises(KeyError):
            ChunkManifest(chunkentries=chunks)

        chunks = {
            "0.0.0": {"path": "s3://bucket/foo.nc", "offset": 100.000, "length": 100},
        }
        with pytest.raises(TypeError, match="must be an int"):
            ChunkManifest(chunkentries=chunks)

    def test_invalid_chunk_keys(self):
        chunks = {
            "0.0.": {"path": "s3://bucket/foo.nc", "offset": 100, "length": 100},
        }
        with pytest.raises(ValueError, match="Invalid format for chunk key: '0.0.'"):
            ChunkManifest(chunkentries=chunks)

        chunks = {
            "0.0": {"path": "s3://bucket/foo.nc", "offset": 100, "length": 100},
            "0": {"path": "s3://bucket/foo.nc", "offset": 200, "length": 100},
        }
        with pytest.raises(ValueError, match="Inconsistent number of dimensions"):
            ChunkManifest(chunkentries=chunks)

        chunks = {
            "0.0.0": {"path": "s3://bucket/foo.nc", "offset": 100, "length": 100},
            "0.0.1": {"path": "s3://bucket/foo.nc", "offset": 200, "length": 100},
            "0.1.0": {"path": "s3://bucket/foo.nc", "offset": 300, "length": 100},
        }
        with pytest.raises(ValueError, match="do not form a complete grid"):
            ChunkManifest(chunkentries=chunks)

        chunks = {
            "1": {"path": "s3://bucket/foo.nc", "offset": 100, "length": 100},
        }
        with pytest.raises(ValueError, match="do not form a complete grid"):
            ChunkManifest(chunkentries=chunks)


class TestSerializeManifest:
    def test_serialize_manifest_to_zarr(self):
        ...

    def test_deserialize_manifest_from_zarr(self):
        ...


def test_create_manifestarray():
    ...


def test_concat():
    ...
