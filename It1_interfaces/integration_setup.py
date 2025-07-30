from subject_impl import CommandSubject
from move_logger_observer import MoveLoggerObserver
from score_observer import ScoreObserver
from sound_effect_observer import SoundEffectObserver
from sound_player import SoundPlayer 
from ScoreManager import ScoreManager

def setup_observers(game_ref=None):
    subject = CommandSubject()

    logger = MoveLoggerObserver()
    scorer = ScoreObserver()
    sound_player = SoundPlayer()  # ← כאן השינוי
    sound = SoundEffectObserver(sound_player)
    
    # יצירת ScoreManager כobserver
    if game_ref:
        score_manager = ScoreManager(game_ref)
    else:
        # ליצור mock game אם לא סופק
        class MockGame:
            pieces = []
        score_manager = ScoreManager(MockGame())

    for event in ["move", "jump", "capture", "reset", "idle"]:
        subject.subscribe(event, logger)
        subject.subscribe(event, sound)
        subject.subscribe(event, score_manager)  # ScoreManager מאזין לכל המהלכים
    subject.subscribe("capture", scorer)

    return subject, logger, scorer, sound_player, score_manager
