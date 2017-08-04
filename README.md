# Overclock

This script will find and open the best available Twitch stream. It will first check any streams that you specify as "priority" streams, then any streams that you follow. If none of those are available, it will open the top stream for the game you specify.

I'm using it, along with an RTC wake-up and `at`, as a sort of alarm clock ([see how](https://medium.com/@acupoftee/building-a-better-alarm-clock-f5feb34e13cd)).

## Usage

1. Install [livestreamer](http://livestreamer.tanuki.se/en/latest/), a command-line utility that will pipe Twitch streams into your video player.
2. Adjust the `config.py` file as you like.
    * Choose your priority channels. These will be checked in your order of preference as `["firstchoice", "secondchoice"]` and so on.
    * Choose the game you would prefer to watch. If none of your priority channels or followed channels are available, the top stream for this game will be opened.
    * Choose the quality of the stream you'd prefer. I'd suggest picking "best" if you can support high-quality video, and "worst" if you cannot. There are other options such as "high", "low", "medium", and "mobile", but they may not always be available depending on the streamer's configuration.
3. If you are running Linux and would like to set the system volume before opening the stream, check if you have `amixer` available (you can do this by typing `amixer -v` in a bash shell and seeing if it gives you a version number). If so, uncomment [this line](https://github.com/molly/streampicker/blob/master/streampicker.py#L119) in `streampicker.py`.
4. Run `streampicker.py`
5. If you have not run the script before, you will be taken to a Twitch webpage to authorize the application. Click "Authorize", then copy the OAuth token it provides into the command prompt.
