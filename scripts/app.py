import logging

from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# --- Check_tag methods ---
@app.route("/<tag_id>", methods=["GET"])
def check_tag(tag_id):
    """
    Checking tag existence in DB (table: tags)

    :param tag_id: Telegram user tag
    :return:
    """

    # Sent data in JSON format
    data = request.get_json()



    return ""


@app.route("/<tag_id>", methods=["POST"])
def check_tag(tag_id):
    """
    Adding a user to the DB (table: tags) with all necessary parameters

    :param tag_id: Telegram user tag
    :return:
    """

    return ""


# --- Check_team_name methods ---
@app.route("/<direction>/<team_name>", methods=["GET"])
def check_team_name(direction, team_name):
    """
    Checking team name existence in DB (table: teams)

    :param direction: One of the directions of the event
    :param team_name: Name of team
    :return:
    """

    return ""


# --- Check_hash methods ---
@app.route("/<direction>/<hash_code>", methods=["GET"])
def check_hash(direction, hash_code):
    """
    Compare the hash_code with the hash_code of the team in the DB (table: teams)

    :param direction: One of the directions of the event
    :param hash_code: Name of team
    :return:
    """

    return ""


# --- Send_result methods ---
@app.route("/<direction>/result", methods=["POST"])
def send_result(direction, result):
    """
    Transfer result to other storage platforms (Google Drive, GitHub) and companies

    :param direction: One of the directions of the event
    :param result: The result of the team's work on the task
    :return:
    """

    return ""


if __name__ == "__main__":
    logging.info("The App is running")

    app.run(host="0.0.0.0", debug=True)
