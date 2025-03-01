import json
import random
import string
import math
import os
from wavetable_data import WAVETABLE_DATA

def random_float(min_val, max_val):
    return min_val + random.random() * (max_val - min_val)

def random_bool():
    return random.choice([0.0, 1.0])

def random_name(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def generate_random_lfo():
    shapes = ["Triangle", "Saw Up", "Square", "Random"]
    return {
        "name": random.choice(shapes),
        "num_points": 3,
        "points": [0.0, 1.0, 0.5, 0.0, 1.0, 1.0],  # Standard wave points
        "powers": [0.0, 0.0, 0.0],
        "smooth": random.choice([True, False])
    }

def generate_random_wavetable():
    return {
        "author": "",
        "full_normalize": False,
        "groups": [
            {
                "components": [
                    {
                        "audio_file": WAVETABLE_DATA['audio_file'],
                        "audio_sample_rate": 44100,
                        "fade_style": 2,
                        "interpolation_style": 1,
                        "keyframes": [
                            {
                                "position": 0,
                                "start_position": 0.0,
                                "window_fade": 1.0,
                                "window_size": 2048.0
                            },
                            {
                                "position": 256,
                                "start_position": 3465.0,
                                "window_fade": 1.0,
                                "window_size": 2048.0
                            }
                        ],
                        "normalize_gain": True,
                        "normalize_mult": False,
                        "phase_style": 2,
                        "random_seed": -919671038,
                        "type": "Audio File Source",
                        "window_size": 1012.9000244140625
                    }
                ]
            }
        ],
        "name": "test",
        "remove_all_dc": False,
        "version": "1.5.5"
    }

def generate_random_modulation(empty_mod_chance=70):
    destinations = [
        # Oscillator 1 parameters
        "osc_1_transpose", "osc_1_tune", "osc_1_level", "osc_1_pan",
        "osc_1_unison_detune", "osc_1_unison_voices", "osc_1_phase",
        "osc_1_random_phase", "osc_1_distortion_mix",
        "osc_1_distortion_drive", "osc_1_spectral_unison_method", "osc_1_spectral_morph_amount",
        "osc_1_spectral_unison_voices", "osc_1_spectral_unison_amount",
        "osc_1_wave_frame", "osc_1_frame_spread", "osc_1_frame_offset",
        
        # Oscillator 2 parameters
        "osc_2_transpose", "osc_2_tune", "osc_2_level", "osc_2_pan",
        "osc_2_unison_detune", "osc_2_unison_voices", "osc_2_phase",
        "osc_2_random_phase", "osc_2_distortion_mix",
        "osc_2_distortion_drive", "osc_2_spectral_unison_method", "osc_2_spectral_morph_amount",
        "osc_2_spectral_unison_voices", "osc_2_spectral_unison_amount",
        "osc_2_wave_frame", "osc_2_frame_spread", "osc_2_frame_offset",
        
        # Oscillator 3 parameters
        "osc_3_transpose", "osc_3_tune", "osc_3_level", "osc_3_pan",
        "osc_3_unison_detune", "osc_3_unison_voices", "osc_3_phase",
        "osc_3_random_phase", "osc_3_distortion_mix",
        "osc_3_distortion_drive", "osc_3_spectral_unison_method", "osc_3_spectral_morph_amount",
        "osc_3_spectral_unison_voices", "osc_3_spectral_unison_amount",
        "osc_3_wave_frame", "osc_3_frame_spread", "osc_3_frame_offset",
        
        # LFO parameters (LFO 1-8)
        *[f"lfo_{i}_delay_time" for i in range(1, 9)],
        *[f"lfo_{i}_fade_time" for i in range(1, 9)],
        *[f"lfo_{i}_frequency" for i in range(1, 9)],
        *[f"lfo_{i}_keytrack_transpose" for i in range(1, 9)],
        *[f"lfo_{i}_keytrack_tune" for i in range(1, 9)],
        *[f"lfo_{i}_phase" for i in range(1, 9)],
        *[f"lfo_{i}_smooth_mode" for i in range(1, 9)],
        *[f"lfo_{i}_smooth_time" for i in range(1, 9)],
        *[f"lfo_{i}_stereo" for i in range(1, 9)],
        
        # Filter 1 parameters
        "filter_1_blend", "filter_1_blend_transpose", "filter_1_cutoff",
        "filter_1_drive", "filter_1_filter_input", "filter_1_formant_resonance",
        "filter_1_formant_spread", "filter_1_formant_transpose", "filter_1_formant_x",
        "filter_1_formant_y", "filter_1_keytrack", "filter_1_mix", "filter_1_model",
        "filter_1_on", "filter_1_resonance", "filter_1_style",
        
        # Filter 2 parameters
        "filter_2_blend", "filter_2_blend_transpose", "filter_2_cutoff",
        "filter_2_drive", "filter_2_filter_input", "filter_2_formant_resonance",
        "filter_2_formant_spread", "filter_2_formant_transpose", "filter_2_formant_x",
        "filter_2_formant_y", "filter_2_keytrack", "filter_2_mix", "filter_2_model",
        "filter_2_on", "filter_2_resonance", "filter_2_style",
        
        # Filter FX parameters
        "filter_fx_blend", "filter_fx_blend_transpose", "filter_fx_cutoff",
        "filter_fx_drive", "filter_fx_formant_resonance", "filter_fx_formant_spread",
        "filter_fx_formant_transpose", "filter_fx_formant_x", "filter_fx_formant_y",
        "filter_fx_keytrack", "filter_fx_mix", "filter_fx_model", "filter_fx_on",
        "filter_fx_resonance", "filter_fx_style",
        
        # Chorus parameters
        "chorus_dry_wet", "chorus_feedback", "chorus_spread", "chorus_delay_2", 
        "chorus_delay_1", "chorus_mod_depth", "chorus_cutoff",
        
        # Compressor parameters
        "compressor_attack", "compressor_high_gain", "compressor_band_gain",
        "compressor_low_gain", "compressor_mix", "compressor_release",
        
        # Delay parameters
        "delay_tempo", "delay_dry_wet", "delay_feedback", "delay_filter_cutoff",
        "delay_filter_spread",
        
        # Distortion parameters
        "distortion_mix", "distortion_filter_blend", "distortion_drive",
        "distortion_filter_cutoff", "distortion_filter_resonance",
        
        # EQ parameters
        "eq_low_resonance", "eq_low_cutoff", "eq_low_gain",
        
        # Flanger parameters
        "flanger_dry_wet", "flanger_mod_depth", "flanger_feedback",
        "flanger_center", "flanger_phase_offset", "flanger_tempo",
        
        # Phaser parameters
        "phaser_dry_wet", "phaser_feedback", "phaser_mod_depth",
        "phaser_center", "phaser_blend", "phaser_tempo",
        "phaser_phase_offset",
        
        # Reverb parameters
        "reverb_dry_wet", "reverb_delay", "reverb_chorus_amount",
        "reverb_low_shelf_cutoff", "reverb_low_shelf_gain",
        "reverb_chorus_frequency", "reverb_size", "reverb_decay_time",
        "reverb_pre_high_cutoff",
        
        # Modulation parameters
        "modulation_3_amount", "modulation_5_amount", "modulation_6_amount",
        "modulation_7_amount", "modulation_8_amount"
    ]
    
    sources = [
        # Envelopes
        "env_1", "env_2", "env_3", "env_4", "env_5", "env_6",
        
        # LFOs
        "lfo_1", "lfo_2", "lfo_3", "lfo_4", "lfo_5", "lfo_6", "lfo_7", "lfo_8",
        
        # Macro controls
        "macro_control_1", "macro_control_2", "macro_control_3", "macro_control_4",
        
        # Performance controls
        "note", "velocity", "mod_wheel", "pitch_wheel", "aftertouch", "lift",
        "random", "stereo"
    ]
    
    if random.random() * 100 < empty_mod_chance:
        return {"destination": "", "source": ""}
    
    return {
        "destination": random.choice(destinations),
        "source": random.choice(sources)
    }

def get_style_ranges(style):
    """Get parameter ranges based on preset style"""
    ranges = {
        "Keys": {
            "polyphony": (4, 32),
            "osc_level": (0.6, 0.9),
            "filter_cutoff": (40, 100),
            "env_attack": (0.1, 0.5),
            "env_decay": (0.4, 0.8),
            "env_sustain": (0.4, 0.8),
            "env_release": (0.3, 0.7)
        },
        "Bass": {
            "polyphony": (1, 4),
            "osc_level": (0.7, 1.0),
            "filter_cutoff": (20, 80),
            "env_attack": (0, 0.3),
            "env_decay": (0.3, 0.6),
            "env_sustain": (0.3, 0.7),
            "env_release": (0.2, 0.5)
        },
        "Lead": {
            "polyphony": (1, 4),
            "osc_level": (0.6, 0.9),
            "filter_cutoff": (40, 120),
            "env_attack": (0, 0.2),
            "env_decay": (0.3, 0.7),
            "env_sustain": (0.4, 0.8),
            "env_release": (0.2, 0.5)
        },
        "Pad": {
            "polyphony": (4, 32),
            "osc_level": (0.5, 0.8),
            "filter_cutoff": (30, 90),
            "env_attack": (0.5, 1.0),
            "env_decay": (0.6, 1.0),
            "env_sustain": (0.6, 1.0),
            "env_release": (0.6, 1.0)
        },
        "Pluck": {
            "polyphony": (4, 16),
            "osc_level": (0.6, 0.9),
            "filter_cutoff": (60, 120),
            "env_attack": (0, 0.1),
            "env_decay": (0.2, 0.5),
            "env_sustain": (0, 0.3),
            "env_release": (0.2, 0.4)
        },
        "FX": {
            "polyphony": (1, 32),
            "osc_level": (0.5, 1.0),
            "filter_cutoff": (20, 120),
            "env_attack": (0, 1.0),
            "env_decay": (0.3, 1.0),
            "env_sustain": (0, 1.0),
            "env_release": (0.3, 1.0)
        },
        "Drums": {
            "polyphony": (1, 8),
            "osc_level": (0.7, 1.0),
            "filter_cutoff": (60, 120),
            "env_attack": (0, 0.1),
            "env_decay": (0.1, 0.4),
            "env_sustain": (0, 0.2),
            "env_release": (0.1, 0.3)
        },
        "Sequence": {
            "polyphony": (4, 16),
            "osc_level": (0.6, 0.9),
            "filter_cutoff": (40, 100),
            "env_attack": (0, 0.2),
            "env_decay": (0.2, 0.5),
            "env_sustain": (0.2, 0.6),
            "env_release": (0.2, 0.5)
        }
    }
    return ranges.get(style, ranges["Keys"])  # Default to Keys if style not found

def generate_random_preset(preset_style="Random", volume_range=(1000, 8000), polyphony_range=(1, 32), empty_mod_chance=70, mod_amount_range=(-1.0, 1.0), mod_power_range=(-4.0, 4.0)):
    preset_styles = ["Keys", "Bass", "Lead", "Pad", "Pluck", "FX", "Drums", "Sequence"]
    
    # If Random style, choose one randomly
    if preset_style == "Random":
        preset_style = random.choice(preset_styles)
    
    # Get parameter ranges based on style
    style_ranges = get_style_ranges(preset_style)
    
    # Update modulation amount ranges to match min/max presets
    modulation_settings = {}
    for i in range(1, 65):
        modulation_settings.update({
            f"modulation_{i}_amount": random_float(*mod_amount_range),  # Use provided range
            f"modulation_{i}_bipolar": random_bool(),
            f"modulation_{i}_bypass": random_bool(),
            f"modulation_{i}_power": random_float(*mod_power_range),  # Use provided range
            f"modulation_{i}_stereo": random_bool()
        })
    
    preset = {
        "author": "RandomPresetGenerator",
        "comments": "Randomly generated preset",
        "macro1": random_name(),
        "macro2": random_name(),
        "macro3": random_name(),
        "macro4": random_name(),
        "preset_style": preset_style,
        "synth_version": "1.5.5",
        "settings": {
            # Basic settings
            "volume": 8000,
            "polyphony": float(random.randint(*polyphony_range)),
            "oversampling": 0.0,
            "beats_per_minute": 2.0,
            "bypass": 0.0,
            
            # Voice settings
            "voice_amplitude": 1.0,
            "voice_override": random_bool(),
            "voice_priority": float(random.randint(0, 8)),
            "voice_transpose": float(random.randint(-24, 24)),
            "voice_tune": random_float(-1, 1),
            
            # Oscillator settings (for each oscillator)
            **{f"osc_{i}_on": random_bool() for i in range(1, 4)},
            **{f"osc_{i}_level": random_float(*style_ranges["osc_level"]) for i in range(1, 4)},
            **{f"osc_{i}_transpose": float(random.randint(-24, 24)) for i in range(1, 4)},
            **{f"osc_{i}_tune": random_float(-1, 1) for i in range(1, 4)},
            **{f"osc_{i}_unison_voices": float(random.randint(1, 8)) for i in range(1, 4)},
            **{f"osc_{i}_unison_detune": random_float(2, 5) for i in range(1, 4)},
            **{f"osc_{i}_unison_blend": random_float(0.5, 1.0) for i in range(1, 4)},
            **{f"osc_{i}_stereo_spread": random_float(0, 1) for i in range(1, 4)},
            **{f"osc_{i}_random_phase": random_bool() for i in range(1, 4)},
            **{f"osc_{i}_phase": random_float(0, 1) for i in range(1, 4)},
            **{f"osc_{i}_midi_track": 1 for i in range(1, 4)},
            **{f"osc_{i}_distortion_type": float(random.randint(0, 12)) for i in range(1, 4)},
            **{f"osc_{i}_spectral_morph_type": float(random.randint(0, 15)) for i in range(1, 4)},
            **{f"osc_{i}_frame_spread": float(0) for i in range(1, 4)},
            **{f"osc_{i}_spectral_morph_amount": random_float(0, 1) for i in range(1, 4)},
            **{f"osc_{i}_spectral_morph_phase": random_float(0, 1) for i in range(1, 4)},
            **{f"osc_{i}_spectral_morph_spread": random_float(0, 1) for i in range(1, 4)},
            
            # Filter settings
            "filter_1_on": random_bool(),
            "filter_1_cutoff": random_float(*style_ranges["filter_cutoff"]),
            "filter_1_resonance": random_float(0, 1),
            "filter_1_blend": random_float(0, 1),
            "filter_1_style": float(random.randint(0, 3)),
            "filter_1_model": float(random.randint(0, 8)),
            "filter_1_drive": random_float(0, 1),
            "filter_1_mix": random_float(0, 1),
            
            # Envelope settings (for each envelope)
            **{f"env_{i}_attack": random_float(*style_ranges["env_attack"]) for i in range(1, 7)},
            **{f"env_{i}_decay": random_float(*style_ranges["env_decay"]) for i in range(1, 7)},
            **{f"env_{i}_sustain": random_float(*style_ranges["env_sustain"]) for i in range(1, 7)},
            **{f"env_{i}_release": random_float(*style_ranges["env_release"]) for i in range(1, 7)},
            **{f"env_{i}_attack_power": random_float(-4, 4) for i in range(1, 7)},
            **{f"env_{i}_decay_power": random_float(-4, 4) for i in range(1, 7)},
            **{f"env_{i}_release_power": random_float(-4, 4) for i in range(1, 7)},
            
            # Effects
            "reverb_on": random_bool(),
            "reverb_decay_time": random_float(-5, 5),
            "reverb_dry_wet": random_float(0, 1),
            "reverb_size": random_float(0, 1),
            "reverb_high_shelf_cutoff": random_float(20, 120),
            "reverb_low_shelf_cutoff": random_float(0, 100),
            
            "delay_on": random_bool(),
            "delay_feedback": random_float(0, 0.95),
            "delay_dry_wet": random_float(0, 1),
            "delay_tempo": float(random.randint(2, 16)),
            
            # LFOs
            "lfos": [generate_random_lfo() for _ in range(8)],
            
            # Modulations
            "modulations": [generate_random_modulation(empty_mod_chance) for _ in range(64)],
            
            # Sample (empty)
            "sample": {
                "length": 0,
                "name": "",
                "sample_rate": 44100,
                "samples": ""
            },
            
            # Wavetables
            "wavetables": [generate_random_wavetable() for _ in range(3)],
            
            # Additional settings
            "stereo_mode": random_bool(),
            "pitch_bend_range": float(random.randint(1, 24)),
            "velocity_track": random_float(0, 1),
            "portamento_time": random_float(-10, 0),
            "legato": random_bool(),
            
            # Macro controls
            "macro_control_1": random_float(0, 1),
            "macro_control_2": random_float(0, 1),
            "macro_control_3": random_float(0, 1),
            "macro_control_4": random_float(0, 1),
            
            # Add all modulation settings
            **modulation_settings
        }
    }
    
    return preset

def save_random_preset(output_dir="random_presets", preset_style="Random", volume_range=(1000, 8000), polyphony_range=(1, 32), empty_mod_chance=70):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate random preset
    preset = generate_random_preset(preset_style, volume_range, polyphony_range, empty_mod_chance)
    
    # Generate random filename
    filename = f"{random_name()}.vital"
    filepath = os.path.join(output_dir, filename)
    
    # Save preset
    with open(filepath, 'w') as f:
        json.dump(preset, f, indent=2)
    
    return filepath

if __name__ == "__main__":
    # Generate 5 random presets as an example
    for i in range(5):
        filepath = save_random_preset()
        print(f"Generated preset: {filepath}") 