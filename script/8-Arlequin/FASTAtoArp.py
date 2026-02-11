

# Loading the FASTA file and the group txt file to understand their structure and content

fasta_file_path = '/mnt/d/Sex_biased_project/7049_sexbi.indel.lowq.het.dp2.mis0.05.mM2.format.fasta' #fasta文件路径
group_file_path = '/mnt/c/Users/Administrator/Desktop/province_20_4910.txt'  #民族_群体分组文件
arp_file_path = '/mnt/c/Users/Administrator/Desktop/中国_province_20_4910.arp'  #结果文件路径
# Read the FASTA file
with open(fasta_file_path, 'r') as file:
    fasta_content = file.readlines()

# Read the Group file
try:
    with open(group_file_path, 'r', encoding='utf-8') as file:
        group_content = file.readlines()
except UnicodeDecodeError:
    # Trying with a more forgiving encoding, assuming the file might have non-standard characters
    with open(group_file_path, 'r', encoding='latin1') as file:
        group_content = file.readlines()

# Inspecting the first few lines of each file to understand their structure
fasta_preview = fasta_content[:5]  # Preview of the FASTA file
group_preview = group_content[:5]  # Preview of the group file

fasta_preview, group_preview

from collections import defaultdict

# Processing the group information to count the number of samples per group
group_dict = defaultdict(list)
for line in group_content:
    sample_name, group_name = line.strip().split('\t')
    group_dict[group_name].append(sample_name)

# Calculating the number of unique groups (NbSamples)
nb_samples = len(group_dict)

# Preparing to match FASTA sequences to their respective groups
# First, create a dictionary to store sequences by sample name for easy lookup
sequence_dict = {}
current_sample_name = ""
for line in fasta_content:
    if line.startswith('>'):
        # Extract sample name, removing the '>'
        current_sample_name = line[1:].strip().split()[0]
        sequence_dict[current_sample_name] = ""
    else:
        # Append sequence lines to the current sample's sequence
        sequence_dict[current_sample_name] += line.strip()

# Now, we can create the .arp file content
arp_content = "[Profile]\n"
arp_content += "   Title = \"Genetic Diversity Analysis\"\n"  # Example title
arp_content += f"   NbSamples = {nb_samples}\n"  # Total number of groups
arp_content += "   DataType = DNA\n"
arp_content += "   GenotypicData = 0\n"
arp_content += "   LocusSeparator = NONE\n"
arp_content += "   MissingData = \"N\"\n"
arp_content += "   CompDistMatrix = 1\n\n"
arp_content += "[Data]\n\n"

# Adding each group's sample information to the .arp file content
for group_name, samples in group_dict.items():
    sample_size = len(samples)  # Number of samples in the group
    arp_content += "[[Samples]]\n"
    arp_content += f"   SampleName = \"{group_name}\"\n"
    arp_content += f"   SampleSize = {sample_size}\n"
    arp_content += "   SampleData= {\n"
    for sample in samples:
        sequence = sequence_dict.get(sample, "N" * 100)  # Fallback to 'N' if not found
        arp_content += f"       {sample} 1 {sequence}\n"
    arp_content += "}\n\n"

# Previewing the beginning of the arp_content
arp_content_preview = "\n".join(arp_content.split('\n')[:20])  # Preview the first few lines
arp_content_preview

# Saving the .arp content to a new file


with open(arp_file_path, 'w', encoding='utf-8') as file:
    file.write(arp_content)