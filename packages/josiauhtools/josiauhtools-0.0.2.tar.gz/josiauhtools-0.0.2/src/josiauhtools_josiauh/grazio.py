"""
Grazio, a custom class to do with gradio.
"""
from enum import Enum
import gradio as gr
import numpy as np
from pydub import AudioSegment
class Themes():
    RedVelvet = gr.themes.Soft(
        primary_hue="rose",
        secondary_hue="cyan",
        neutral_hue="slate",
    )

class Interfaces:
    class Examples:
        class News:
            def __new__(s):
                def news(name):
                    choicesList = ["Amusement park dies in summer due to snow!", "Fluxus being sued by Flies!", "Reporters still setting up live!"]
                    return f"Hey guys! {name} here. Breaking news! {np.random.choice(choicesList)}"
                return gr.Interface(
                    fn=news,
                    inputs=["text"],
                    outputs=["text"]
                )
