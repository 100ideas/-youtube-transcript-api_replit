##########################################
# hello-world example of youtube-transcript-youtube_transcript_api
# https://github.com/jdepoix/youtube-transcript-api#by-example
# 21 aug 2020
##########################################


from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api.formatters import PrettyPrintFormatter
from youtube_transcript_api.formatters import WebVTTFormatter

import string
import re
import textwrap


# retrieve the available transcripts
transcript_list = YouTubeTranscriptApi.list_transcripts('jGJT1FRYGcY')
# transcript_list = YouTubeTranscriptApi.get_transcripts('jGJT1FRYGcY')
# transcript_list = YouTubeTranscriptApi.get_transcripts('jGJT1FRYGcY', languages=['en'])

# iterate over all available transcripts

fetched = 'NOT_FETCHED'

for transcript in transcript_list:
    if transcript.language_code == 'en':
        # the Transcript object provides metadata properties
        print(
            '[ID]: ' + transcript.video_id,
            '[lang]: ' + transcript.language_code,
            # whether it has been manually created or generated by YouTube
            '[autogenerated]: ' + str(transcript.is_generated),
            # whether this transcript can be translated or not
            '[translatable]: ' + str(transcript.is_translatable),
            # a list of languages the transcript can be translated to
            # transcript.translation_languages,
            '\n'
        )
        fetched = transcript.fetch()
        break

    # translating the transcript will return another transcript object
    # print(transcript.translate('en').fetch())

    # you can also directly filter for the language you are looking for, using the transcript list
    # transcript = transcript_list.find_transcript(['en'])  



############################################################
# util function from src
# https://github.com/jdepoix/youtube-transcript-api/blob/c5bf0132ffa2906cc1bf6d480a70ef799dedc209/youtube_transcript_api/formatters.py#L84
#
def _seconds_to_timestamp(time):
      """Helper that converts `time` into a transcript cue timestamp.
      :reference: https://www.w3.org/TR/webvtt1/#webvtt-timestamp
      :param time: a float representing time in seconds.
      :type time: float
      :return: a string formatted as a cue timestamp, 'HH:MM:SS.MS'
      :rtype str
      :example:
      >>> self._seconds_to_timestamp(6.93)
      '00:00:06.930'
      """
      time = float(time)
      hours, mins, secs = (
          int(time) // 3600,
          int(time) // 60,
          int(time) % 60,
      )
      ms = int(round((time - int(time))*1000, 2))
      return "{:02d}:{:02d}:{:02d}.{:03d}".format(hours, mins, secs, ms)
############################################################



wrapper = textwrap.TextWrapper(width=70, fix_sentence_endings=True, drop_whitespace=True)
length = 0
cap= ''
begin = 0.0
end = 0.0

for line in fetched:

    cap = cap + line['text']
    end += line['duration']

    # accumulate sentences into small legible paragraphs 
    if (cap.endswith(('.', ':', '!', '?')) and ((end - begin > 10.0) or (len(cap) > 100))):
        # fix whitespaces errors around punctuation
        cap = re.sub(r'([{}])'.format('.!?:,'),r'\1 ',cap) 
        cap = cap.replace('  ', ' ')
        cap = wrapper.fill(text=cap) + '\n'
        # print((_seconds_to_timestamp(begin) + '  [' + str(length) + ']').rjust(70))
        print(_seconds_to_timestamp(begin).rjust(70))
        print(cap)
        cap = ''
        begin = end



############################################################
## play w/ built-in formatters

# pretty = PrettyPrintFormatter().format_transcript(transcript.fetch())
# plain = TextFormatter().format_transcript(fetched)
# vtt = WebVTTFormatter().format_transcript(fetched)

# print(pretty[length], sep='\n')
# print(vtt)
# print(formatted)