# PastFm

**YT Music now playing card for my github profile**

## Description
PastFm is a simple tool that retrieves and displays the last played songs from **YouTube Music**.

## Flowchart
![flowchart](static/image-1.png)

## Installation & Usage
1. Clone this repository:
   ```sh
   git clone https://github.com/arpy8/PastFm.git
   ```
2. Navigate to the project folder:
   ```sh
   cd PastFm
   ```
3. Setup your own [api](https://huggingface.co/spaces/arpy8/PastFm-Backend) on HF Spaces
4. Replace the api url in the extension's code and install the PastFm[extension](./extension/) in your browser.

## Setting up the Python API with `uv`
1. Setup the project using:
   ```sh
   uv venv
   ```
2. Install dependencies:
   ```sh
   uv pip install -r requirements.txt
   ```
3. Run the API:
   ```sh
   uvicorn api:app --host 0.0.0.0 --port 7860
   ```
   or 
   ```sh
   python api.py
   ```

## Live Preview
Check out the live rendering of the fetched songs:

<a href="https://arpy8-pastfm-backend.hf.space/redirect">
    <img src="https://arpy8-pastfm-backend.hf.space/live" alt="" />
</a>

## Contributing
Contributions are welcome! Feel free to fork the repo and submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

## Built With
- **HTML, CSS** for UI
- **JavaScript** for service worker
- **Fasapi** for API development
- **Huggingface Spaces** for hosting

## Author
Made with ♪ by [arpy8](https://arpy8.com)  
