import pytumblr
import Wheather_API as weather

CONSUMER_KEY = "RtOjOZS7bdEkRaoM7SE45L490aljmTfrCAny5rtGHDEzFvY4gg"
CONSUMER_SECRET = 'q8wAsJPh55B4SJ5nVGpZgHCxxHNJ6C3sMp1fw64pggQS8lojoy'

client = pytumblr.TumblrRestClient(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    'ItzSp75ezZF8o1aYTKyczeIniIUrMARjtkgprEVpxZgYvSDHpF',  # Oauth token
    'ogBBYQ9kUqxoRGnJl8cxH4Ha5PAhVOZkI5fjLovGLAWYzBEymI'  # Oauth secret
)


def post_weather_on_tumblr():
    my_weather = weather.get_weather()

    text = ""
    text += "The weather in " + my_weather['sys']['country'] + "," + my_weather['name'] + " "
    text += "is " + my_weather['weather'][0]['main'] + " with a description of : " + my_weather['weather'][0][
        'description']
    print(text)

    res = client.create_text("awesome-arvinte-razvan", state="published", slug="Could_Lab1",
                             title="Weather at my location",
                             body=text)

    return res


post_weather_on_tumblr()
