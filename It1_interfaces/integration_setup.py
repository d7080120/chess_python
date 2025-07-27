from subject_impl import CommandSubject
from move_logger_observer import MoveLoggerObserver
from score_observer import ScoreObserver
from sound_effect_observer import SoundEffectObserver
from sound_player import SoundPlayer 
def setup_observers():
    subject = CommandSubject()

    logger = MoveLoggerObserver()
    scorer = ScoreObserver()
    sound_player = SoundPlayer()  # ← כאן השינוי
    sound = SoundEffectObserver(sound_player)

    for event in ["move", "jump", "capture", "reset", "idle"]:
        subject.subscribe(event, logger)
        subject.subscribe(event, sound)
    subject.subscribe("capture", scorer)

    return subject, logger, scorer, sound_player
