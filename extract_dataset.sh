#!/bin/bash

# Base directory where all the downloaded files are
base_dir="SkyScenes"

# Find all .tar.gz files recursively
find "$base_dir" -type f -name "*.tar.gz" | while read -r file; do
    echo "Extracting: $file"
    
    # Get the directory containing the tar file
    dir=$(dirname "$file")
    
    # Extract the tar file (without gzip decompression)
    tar xf "$file" -C "$dir"
    
    # Remove the tar file after successful extraction
    if [ $? -eq 0 ]; then
        echo "Removing: $file"
        rm "$file"
    else
        echo "Error extracting $file"
    fi
done

echo "Extraction complete!"