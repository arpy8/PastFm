# PastFm
**Last.fm Scrobble Card for My GitHub Profile**

## Why I made this
I had been using the [spotify-github-profile](https://github.com/kittinan/spotify-github-profile) banner for a long time. But ever since spotify people decided to ban their modded app, I found myself jumping between different platforms to listen to music. Hence I wanted this banner to showcase my listening activity from every platform, so I made a custom version for me!
Also huge shoutout to [kittinan](https://github.com/kittinan). I used his default theme for the card, so it looks somewhat similar.

## Note
A same copy of this repository can be found on huggingface as well, where I've hosted the API.

[PastFm Backend - HF Spaces](https://huggingface.com/spaces/arpy8/pastfm-backend)

## Usage  
1. Sign up for a Last.fm account and connect your Spotify or another music platform.  
2. Add the following line to your README:  

   ```  
   ![](https://arpy8-pastfm-backend.hf.space/live?user=<your-lastfm-username>)  
   ```

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
