# Video Compressor Project

This project compresses `.mp4` files with the word "trim" in the filename, renames them sequentially (e.g., Clip (1), Clip (2)), and moves them to the `clips_folder`.

## Requirements

1. Docker
2. Python (for local development)

## How to Run the Project in Docker

1. Clone the repository.
2. Build the Docker image: `docker build -t video_compressor`

3. Run the Docker container with folder bindings:
`docker run -v /path/to/input_folder:/input_folder -v /path/to/clips_folder:/clips_folder video_compressor`

## Folder Structure

- `input_folder/`: Drop `.mp4` files here to be processed.
- `clips_folder/`: Processed and compressed video files will be saved here.