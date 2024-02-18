#!/bin/bash

# Print usage instructions
print_usage() {
  echo "Usage: $0 -a <audiofile> -l <lyricsfile> [-p <true/false>]"
  echo "Options:"
  echo "  -a, --audiofile     Path to the vocal audio file"
  echo "  -l, --lyricsfile    Path to the lyrics text file"
  echo "  -p, --append_pipe   Expose lyrics line breaks to NFA (Default: true)"
  echo "Example:"
  echo "  $0 -a audio.wav -l lyrics.txt -p true"
}

# Define default values
append_pipe=true

# Parse command-line options
while getopts ":a:l:p:" opt; do
  case ${opt} in
    a )
      audiofile=$(realpath -m "$OPTARG")
      audiofile_dir=$(dirname "$audiofile")
      ;;
    l )
      lyricsfile=$(realpath -m "$OPTARG")
      ;;
    p )
      append_pipe=$OPTARG
      ;;
    \? )
      echo "Invalid option: $OPTARG" 1>&2
      print_usage
      exit 1
      ;;
    : )
      echo "Invalid option: $OPTARG requires an argument" 1>&2
      print_usage
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

# Check if required arguments are provided
if [ -z "$audiofile" ] || [ -z "$lyricsfile" ]; then
  echo "Error: Both audiofile and lyricsfile are required." 1>&2
  print_usage
  exit 1
fi

# Call Python script with the provided arguments
python prepare.py --audiofile "$audiofile" --lyricsfile "$lyricsfile" --append_pipe "$append_pipe"
python NeMo/tools/nemo_forced_aligner/align.py  pretrained_name="stt_en_fastconformer_hybrid_large_pc" manifest_filepath="$audiofile.manifest.json"  output_dir="$audiofile_dir/nfa_output/" additional_segment_grouping_separator="|"

# Check if a tokens CTM file was written and if so how many lines it is
echo
output_file="$audiofile_dir/nfa_output/ctm/tokens/$(basename "$audiofile" | tr ' ' '-').prepared.ctm"
echo "Output should be at $output_file..."
echo
if [ -f "$output_file" ]; then
  num_lines=$(wc -l < "$output_file")
  echo "Complete!  NFA wrote $num_lines tokens."
else
  echo "Hmm, I don't see it, so something may have gone wrong."
fi