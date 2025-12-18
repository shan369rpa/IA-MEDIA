import json

input_data = [
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 0.0,
        "end": 0.5839166666666666,
        "type": "audio_filter",
        "details": {
          "name": "Audio Crossfade"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 3.128125,
        "end": 3.7120416666666665,
        "type": "audio_filter",
        "details": {
          "name": "Audio Crossfade"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 3.4200833333333334,
        "end": 12.303958333333334,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 3.4200833333333334,
        "end": 12.303958333333334,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 3.4200833333333334,
        "end": 12.303958333333334,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 3.4200833333333334,
        "end": 12.303958333333334,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 12.012,
        "end": 12.595916666666668,
        "type": "audio_filter",
        "details": {
          "name": "Audio Crossfade"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 12.303958333333334,
        "end": 30.238541666666666,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 12.303958333333334,
        "end": 30.238541666666666,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 12.303958333333334,
        "end": 30.238541666666666,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 12.303958333333334,
        "end": 30.238541666666666,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 30.238541666666666,
        "end": 57.47408333333333,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 30.238541666666666,
        "end": 57.47408333333333,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 30.238541666666666,
        "end": 57.47408333333333,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 30.238541666666666,
        "end": 57.47408333333333,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 57.47408333333333,
        "end": 679.7207083333333,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 57.47408333333333,
        "end": 679.7207083333333,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 57.47408333333333,
        "end": 679.7207083333333,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 57.47408333333333,
        "end": 679.7207083333333,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 679.7207083333333,
        "end": 835.6264583333333,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 679.7207083333333,
        "end": 835.6264583333333,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 679.7207083333333,
        "end": 835.6264583333333,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 679.7207083333333,
        "end": 835.6264583333333,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 835.6264583333333,
        "end": 912.16125,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 835.6264583333333,
        "end": 912.16125,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 835.6264583333333,
        "end": 912.16125,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 835.6264583333333,
        "end": 912.16125,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 911.8692916666666,
        "end": 912.4532083333334,
        "type": "audio_filter",
        "details": {
          "name": "Audio Crossfade"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 912.16125,
        "end": 1056.6389166666668,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 912.16125,
        "end": 1056.6389166666668,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 912.16125,
        "end": 1056.6389166666668,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 912.16125,
        "end": 1056.6389166666668,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1056.3469583333333,
        "end": 1056.930875,
        "type": "audio_filter",
        "details": {
          "name": "Audio Crossfade"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1056.6389166666668,
        "end": 1194.9020416666667,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1056.6389166666668,
        "end": 1194.9020416666667,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1056.6389166666668,
        "end": 1194.9020416666667,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1056.6389166666668,
        "end": 1194.9020416666667,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1194.6100833333333,
        "end": 1195.194,
        "type": "audio_filter",
        "details": {
          "name": "Audio Crossfade"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1194.9020416666667,
        "end": 1195.2357083333334,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1194.9020416666667,
        "end": 1195.2357083333334,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1194.9020416666667,
        "end": 1195.2357083333334,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1195.2357083333334,
        "end": 1615.1969166666668,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1195.2357083333334,
        "end": 1615.1969166666668,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1195.2357083333334,
        "end": 1615.1969166666668,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1195.2357083333334,
        "end": 1615.1969166666668,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1615.1969166666668,
        "end": 1724.5978750000002,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1615.1969166666668,
        "end": 1724.5978750000002,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1615.1969166666668,
        "end": 1724.5978750000002,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1615.1969166666668,
        "end": 1724.5978750000002,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1724.3059166666667,
        "end": 1724.8898333333334,
        "type": "audio_filter",
        "details": {
          "name": "Audio Crossfade"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1724.597875,
        "end": 1758.381625,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1724.597875,
        "end": 1758.381625,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1724.597875,
        "end": 1758.381625,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1724.597875,
        "end": 1758.381625,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1758.0896666666667,
        "end": 1758.6735833333335,
        "type": "audio_filter",
        "details": {
          "name": "Audio Crossfade"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 2475.3226000000004,
        "end": 2475.3895833333336,
        "type": "fadeout",
        "details": {
          "type": "easeIn",
          "duration": "48228/720000s"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1758.381625,
        "end": 2475.3895833333336,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1758.381625,
        "end": 2475.3895833333336,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1758.381625,
        "end": 2475.3895833333336,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 1758.381625,
        "end": 2475.3895833333336,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 2475.389583333333,
        "end": 2833.4973333333332,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 2475.389583333333,
        "end": 2833.4973333333332,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 2475.389583333333,
        "end": 2833.4973333333332,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 2475.389583333333,
        "end": 2833.4973333333332,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 2833.205375,
        "end": 2833.7892916666665,
        "type": "audio_filter",
        "details": {
          "name": "Audio Crossfade"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 2833.4973333333332,
        "end": 2837.4179166666668,
        "type": "audio_filter",
        "details": {
          "name": "Gain"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 2833.4973333333332,
        "end": 2837.4179166666668,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 2833.4973333333332,
        "end": 2837.4179166666668,
        "type": "audio_filter",
        "details": {
          "name": "Compressor"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 2833.4973333333332,
        "end": 2837.4179166666668,
        "type": "audio_filter",
        "details": {
          "name": "Channel EQ"
        }
      },
      {
        "session_id": "1992.11.22-giác ngộ có sẵn trong ta",
        "start": 2836.834,
        "end": 2837.4179166666663,
        "type": "audio_filter",
        "details": {
          "name": "Audio Crossfade"
        }
      }
    ]


seen = set()
unique_list = []

for item in input_data:
    key = (item["type"], item["details"]["name"])
    if key not in seen:
        seen.add(key)
        unique_list.append(item)

# Ghi ra file result.json
with open("unique.json", "w", encoding="utf-8") as f:
    json.dump(unique_list, f, indent=2, ensure_ascii=False)

print("Done! Unique by (type + details.name)")
