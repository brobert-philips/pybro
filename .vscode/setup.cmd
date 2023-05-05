cargo build --release
cp target/release/libdicom.dylib src/pybro/dicom/rust_dicom.so

python -m pdoc -d numpy --math -o docs src/pybro
pytest -v
