translate
=========

Use google translate to translate words.
Google translate API is a paid service, so this program should not work a long time.

## Help

    $ ./translate.py -h
    usage: translate.py [-h] [-i LANGUAGE] [-o LANGUAGE] TEXT

    Translate text using google services

    positional arguments:
      TEXT                  Text to translate

    optional arguments:
      -h, --help            show this help message and exit
      -i LANGUAGE, --input LANGUAGE
                            Input Language (default fr)
      -o LANGUAGE, --output LANGUAGE
                            Output Language (default en)

## Example

    $ ./translate.py -i fr -o en chien
    dog
    dog    => chien,mâle,fille moche
    hound  => chien,chien de chasse,chien de meute,acharnement,canaille,basset
    cock   => coq,robinet,bite,mâle,chien,bitte
    hanger => cintre,crochet,portemanteau,exécuteur,bourreau,chien
