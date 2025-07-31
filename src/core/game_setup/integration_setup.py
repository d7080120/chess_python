from src.core.observers.subject_impl import CommandSubject
from src.core.observers.move_logger_observer import MoveLoggerObserver
from src.core.observers.score_observer import ScoreObserver
from src.core.observers.sound_effect_observer import SoundEffectObserver
from src.ui.sound_player import SoundPlayer 
from src.core.observers.ScoreManager import ScoreManager

def setup_observers(game_ref=None):
    subject = CommandSubject()

    logger = MoveLoggerObserver()
    scorer = ScoreObserver()
    sound_player = SoundPlayer()  # ← כאן השינוי
    sound = SoundEffectObserver(sound_player)
    
    print(f"DEBUG: Sound system initialized - SoundPlayer: {type(sound_player)}, SoundEffectObserver: {type(sound)}")
    
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
    
    print(f"DEBUG: Observers registered for sound system - Events: move, jump, capture, reset, idle")

    return subject, logger, scorer, sound_player, score_manager
