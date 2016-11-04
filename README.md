# lektor-minification

A simple [Lektor](https://www.getlektor.com/) plugin to minify images at build time.

## Requirements

Some packages have to be installed beforehand the plugin installation.

**Linux :**

	$ sudo apt-get install -y optipng jpegoptim libjpeg8-dev zlib1g-dev gifsicle

**OS X :**

	$ brew install optipng jpegoptim gifsicle libmagic

## Installation

The easier is to use the command line :

	$ lektor plugins add lektor-minification

But you could also add the plugin to your `.lektorproject` file, so it'll be automatically downloaded by Lektor :

```ini
[packages]
lektor-minification = 1.1.3
```

## How to use

There's nothing more to do ! The plugin will optimize on-the-fly all the PNG and JPEG images each time that you're building your project :

	$ lektor build

## Configuration

You can edit the `config.yml` file to tweak the optimization tools and their options, as explained in the [pyimagediet documentation](http://pyimagediet.readthedocs.io/en/latest/configure.html).

Just be sure to always keep something to execute for each file type (png, jpeg and gif) or the build process could crash.

## Support

This plugin is provided as-is by [NumeriCube](http://numericube.com), a human-sized Paris-based company prodiving tailored services to smart customers. 

We'd be happy to try to help you with this plugin if needed. In that case, just file an issue on the [GitHub tracker](https://github.com/numericube/lektor-minification/issues).

## License

lektor-minification is released under the [GNU General Public License v3](https://github.com/numericube/lektor-minification/blob/master/LICENSE).

## Contributing

You can submit any ideas, suggestions or bug reports to our [GitHub tracker](https://github.com/numericube/lektor-minification/issues).

If you'd like to merge any bug fix or enhancement into the project, please fill a [pull request](https://github.com/numericube/lektor-minification/pulls).
