import argparse
import requests
import pprint

def main():

    api_url = "https://script.google.com/macros/s/AKfycbzKjxnq7rQOY-GDPHIheMeRJ0k_Xc29Xmvi4GL808KFuCQ9pa7DmNGRffAC7qChVoTC/exec"
    ##headers = {"Authorization": "Bearer ya29.***************************************************************************************************************"}

    parser = argparse.ArgumentParser()
    parser.add_argument("-input", type=str, required=True)
    args = parser.parse_args()

    input = ""
    with open(args.input, 'r',encoding="utf-8") as f:
        for line in f:
            print(line)
            line = line.strip()
            input += line

    params = {
        'text': "\"" + input + "\"",
        'source': 'en',
        'target': 'ja'
    }

    ##r_post = requests.post(api_url, headers=headers, data=params)
    r_post = requests.post(api_url, data=params)
    print(r_post.text)


if __name__ == "__main__":
    main()
