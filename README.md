# KNX User Forum Icon Set

Icon set from [KNX User Forum](https://knx-user-forum.de/forum/playground/knx-uf-iconset) for Home Assistant. The icon set contains more than 900 icons for home automation.

## Installation

1. Ensure that [HACS](https://hacs.xyz) is installed.
2. Open `Frontend` tab in HACS and install "KNX User Forum Icon Set".
3. Reload browser cache.

### Manual Installation

1. Copy `ha-knx-uf-iconset.js` from the `dist` directory of this repository into the subdirectory `www` of the Home Assistant configuration directory (where your `configuration.yaml` resides).
2. Open `Configuration -> Lovelace Dashboards -> Resources`.
3. Add a new resource with URL = `/local/ha-knx-uf-iconset.js` and Resource type = `JavaScript Module`.
4. Reload your browser cache.

## Usage

An overview of all available icons can be found can in the [Icon Set Generator](https://service.knx-user-forum.de/?comm=iconset).

Remember the icon name, e.g. `audio_audio`, and prefix it with `kuf`.

Example:

`kuf:audio_audio`

## Credits

Icons are based on the icon set provided by [https://github.com/OpenAutomationProject/knx-uf-iconset](https://github.com/OpenAutomationProject/knx-uf-iconset) licensed by [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/deed.en). Combined paths and converted strokes to paths for SVG files. Many thanks for your work!
