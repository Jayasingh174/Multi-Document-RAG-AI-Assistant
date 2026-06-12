import subprocess
import os

ODA_PATH = r"C:\Jaya\ODA\ODAFileConverter 27.1.0\ODAFileConverter.exe"

def convert_dwg_to_dxf(dwg_path: str):

    if not os.path.exists(ODA_PATH):
        raise FileNotFoundError("ODA File Converter not found")

    if not os.path.exists(dwg_path):
        raise FileNotFoundError("DWG file not found")

    input_dir = os.path.dirname(dwg_path)
    output_dir = input_dir

    base_name = os.path.splitext(os.path.basename(dwg_path))[0]
    dxf_path = os.path.join(output_dir, base_name + ".dxf")

    cmd = [
        ODA_PATH,
        input_dir,
        output_dir,
        "ACAD2018",
        "DXF",
        "0",
        "1",
        "*.DWG"
    ]

    print("Running ODA Converter:", cmd)

    result = subprocess.run(cmd, capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    if not os.path.exists(dxf_path):
        raise ValueError("DWG conversion failed - DXF not generated")

    return dxf_path