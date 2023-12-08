import subprocess
from typing import Optional
from typeguard import typechecked


@typechecked
def R1(
    file_path: str,
    spacer_tag: str,
    barcode_tag: Optional[str] = None,
    stub_tag: Optional[str] = None,
    hamming_distance: int = 0,
) -> str:
    
    R1_regex = ""

    if barcode_tag:
        R1_barcode_info = subprocess.run(["seqspec", "find", "-m", "crispr", "-r", barcode_tag, file_path], capture_output=True, text=True)
        R1_barcode_info = str(R1_barcode_info.stdout).split("\n")

        min_len = None
        max_len = None

        for line in R1_barcode_info:
            if "min_len" in line:
                position = line.find("min_len")
                min_len = line[position + 9:]
            if "max_len" in line:
                position = line.find("max_len")
                max_len = line[position + 9:]  

        R1_regex += "'^(?P<cell_1>.{" + min_len + "," + max_len + "})"

    if stub_tag:
        stub_info = subprocess.run(["seqspec", "find", "-m", "crispr", "-r", stub_tag, file_path], capture_output=True, text=True)
        stub_info = str(stub_info.stdout).split("\n")

        stub_sequence = None

        for line in stub_info:
            if "sequence:" in line:
                position = line.find("sequence:")
                stub_sequence = line[position + 10:]

        R1_regex += "(?P<discard_1>" + stub_sequence + ")"  
        
    spacer_info = subprocess.run(["seqspec", "find", "-m", "crispr", "-r", spacer_tag, file_path], capture_output=True, text=True)
    spacer_info = str(spacer_info.stdout).split("\n")

    spacer_len = None

    for line in spacer_info:
        if "max_len" in line:
            position = line.find("max_len")
            spacer_len = line[position + 9:]

    R1_regex += "{s<=" + str(hamming_distance) + "}(?P<guide_1>.{" + spacer_len + "})(?P<discard_2>.+)$'"

    return R1_regex


#make barcode optional
@typechecked
def R2(
    file_path: str,
    reporter_tag: str, 
    barcode_tag: Optional[str] = None,
) -> str:
    
    R2_regex = ""

    if barcode_tag:
        R2_barcode_info = subprocess.run(["seqspec", "find", "-m", "crispr", "-r", barcode_tag, file_path], capture_output=True, text=True)
        R2_barcode_info = str(R2_barcode_info.stdout).split("\n")

        barcode_len = None

        for line in R2_barcode_info:
            if "max_len" in line:
                position = line.find("max_len")
                barcode_len = line[position + 9:]

        R2_regex += "'^(?P<umi_1>.{" + barcode_len + "})"

    reporter_info = subprocess.run(["seqspec", "find", "-m", "crispr", "-r", reporter_tag, file_path], capture_output=True, text=True)
    reporter_info = str(reporter_info.stdout).split("\n")

    reporter_len = None

    for line in reporter_info:
        if "max_len" in line:
            position = line.find("max_len")
            reporter_len = line[position + 9:]

    
    R2_regex += "(?P<surrogate_1>.{" + reporter_len + "})(?P<discard_1>.+)$'"

    return R2_regex