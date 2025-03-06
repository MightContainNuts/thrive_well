from application.utils.gemini_ai_handler import GeminiAIHandler
from application.utils.open_ai_handler import OpenAIHandler
from application.utils.groq_ai_handler import GroqAIHandler
from concurrent.futures import ThreadPoolExecutor


journal_entry = """
Dear Diary,

I woke up this morning with a sense of hope—well, as much hope as one can have
when surrounded by lava pits and an army of orcs. You know, it’s really hard to
stay positive when the ground you walk on feels like it’s trying to eat you.
But I digress… Frodo says “We’re almost there,” but he looks like he hasn’t
had a proper meal in days. I mean, the guy’s turning into a walking bag of
bones, and I’m starting to think the Ring is his only food group. Maybe we
should’ve stopped for breakfast in Rivendell, huh?
And then there’s Sam, who, bless him, is trying to keep spirits up with his
potato recipes. I mean, if I hear one more “It’s the best potato in the world!”
line, I might throw myself into Mount Doom just to escape the endless spuds.
But then again, Sam’s really just trying to keep us all from falling into
despair. So, kudos to him. But let’s talk about Gollum. I’ve never met someone
so conflicted in my life. One minute he’s trying to steal the Ring back, and
the next he’s singing us songs about how preciousit is. If I didn’t know
better, I’d say he’s the walking embodiment of bipolar—just without the
charming smile. Seriously, that guy can go from “I love you, master!” to “I’m
going to eat your face” in less than five seconds. If there’s one thing I’ve
learned, it’s to never let Gollum handle the maps. He’s absolutely terrible
with directions. Oh, and speaking of terrible, Aragorn decided today was the
perfect time for one of his inspirational speeches about destiny and bravery.
I swear, every time he starts one of these, Legolas and Gimli try their best
to look interested, but we all know they’d rather be doing literally anything
else, like fighting a Balrog or swimming in the Dead Sea.
Anyway, I’m ending the day feeling somewhat optimistic. I mean, I haven’t
fallen into the lava (yet), and my sword’s still shiny. But who knows?
Tomorrow could be another battle,another ambush, or another lecture from
Gandalf. But it’ll be an adventure, right? Maybe we’ll actually get to the
Mountain by next century!
Until then, here’s to not getting eaten by orcs today!
With mixed emotions and a slight headache,
Aragorn (The Slightly Disappointed)
"""


def thread_1():
    handler = GeminiAIHandler()
    response = handler.create_journal_entry_response(journal_entry)
    print("Gemini AI Handler")
    print("-" * 50)
    print(response)
    print("-" * 50)
    return response


def thread_2():
    openai_handler = OpenAIHandler()
    response = openai_handler.create_journal_entry_response(journal_entry)
    print("Open AI Handler")
    print("-" * 50)
    print(response)
    print("-" * 50)
    return response


def thread_3():
    openai_handler = GroqAIHandler()
    response = openai_handler.create_journal_entry_response(journal_entry)
    print("Open Grok Handler")
    print("-" * 50)
    print(response)
    print("-" * 50)
    return response


def run_in_threads():
    results = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(thread_1),
            executor.submit(thread_2),
            executor.submit(thread_3),
        ]

        for future in futures:
            results.append(future.result())
        return results


def main():

    run_in_threads()


if __name__ == "__main__":
    main()
