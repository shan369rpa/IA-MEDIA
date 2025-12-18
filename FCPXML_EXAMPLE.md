# Báo cáo Phân tích FCPXML - FCPXML_ANALYSIS_BATCH_02_v2

- **Tổng số file FCPXML đã phân tích:** 9
- **Danh sách Session ID:**
  - `1992.11.22-giác ngộ có sẵn trong ta`
  - `2000.03.19-trí tuệ là sự nghiệp lớn nhất`
  - `2001.07.13-khổ đau vì tiêu thụ`
  - `2001.08.07-sống hạnh phúc chết bình an`
  - `2003.04.03-tình yêu chân thật`
  - `2004.09.19-đối phó với cơn bão trong lòng`
  - `2009.11.29-điềm lành lớn nhất`
  - `2012.02.19-linh đan đổi cốt mới ra về`
  - `2014.07.29-hãy thương nhau đi`

---
## 2. Thống kê Tần suất Thẻ trên Toàn bộ các File

| Tag Name | Tổng số lần XH | Số File có Chứa Thẻ này |
| :--- | :--- | :--- |
| `adjust-EQ` | 141 | 4/9 |
| `adjust-colorConform` | 41 | 1/9 |
| `adjust-humReduction` | 8 | 1/9 |
| `adjust-loudness` | 60 | 1/9 |
| `adjust-noiseReduction` | 288 | 9/9 |
| `adjust-panner` | 53 | 2/9 |
| `adjust-transform` | 294 | 8/9 |
| `adjust-voiceIsolation` | 213 | 7/9 |
| `adjust-volume` | 297 | 9/9 |
| `array` | 10 | 9/9 |
| `asset` | 19 | 9/9 |
| `asset-clip` | 313 | 9/9 |
| `audio-channel-source` | 297 | 9/9 |
| `bookmark` | 19 | 9/9 |
| `caption` | 46 | 6/9 |
| `clip` | 1 | 1/9 |
| `conform-rate` | 274 | 8/9 |
| `data` | 1346 | 9/9 |
| `effect` | 73 | 9/9 |
| `event` | 9 | 9/9 |
| `fadeIn` | 8 | 3/9 |
| `fadeOut` | 15 | 5/9 |
| `fcpxml` | 9 | 9/9 |
| `filter-audio` | 1148 | 9/9 |
| `filter-video` | 1006 | 9/9 |
| `format` | 27 | 9/9 |
| `keyframe` | 4833630 | 9/9 |
| `keyframeAnimation` | 297 | 9/9 |
| `keyword` | 99 | 4/9 |
| `keyword-collection` | 17 | 1/9 |
| `library` | 9 | 9/9 |
| `marker` | 199 | 6/9 |
| `match-clip` | 8 | 8/9 |
| `match-media` | 32 | 8/9 |
| `match-ratings` | 8 | 8/9 |
| `md` | 105 | 9/9 |
| `media-rep` | 19 | 9/9 |
| `metadata` | 19 | 9/9 |
| `param` | 9828 | 9/9 |
| `project` | 9 | 9/9 |
| `rating` | 2 | 1/9 |
| `resources` | 9 | 9/9 |
| `sequence` | 9 | 9/9 |
| `smart-collection` | 40 | 8/9 |
| `spine` | 9 | 9/9 |
| `string` | 20 | 9/9 |
| `text` | 49 | 6/9 |
| `text-style` | 98 | 6/9 |
| `text-style-def` | 49 | 6/9 |
| `title` | 3 | 2/9 |
| `transition` | 214 | 9/9 |
| `video` | 10 | 9/9 |

---
## 3. Phân tích Chuyên sâu theo Từng Loại Chỉnh sửa Âm thanh

### 3.1. audio_filter
- **Tần suất:** Xuất hiện **1148** lần trong **9/9** file.
- **Thời lượng trung bình:** 92.66 giây.
- **Ví dụ (từ `1992.11.22-giác ngộ có sẵn trong ta`):**
  ```json
  [
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
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 4.546208333333333,
    "end": 5.171833333333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 4.879875,
    "end": 31.322958333333332,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 4.879875,
    "end": 31.322958333333332,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 4.879875,
    "end": 31.322958333333332,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 31.031,
    "end": 31.614916666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 31.322958333333332,
    "end": 43.126416666666664,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 31.322958333333332,
    "end": 43.126416666666664,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 31.322958333333332,
    "end": 43.126416666666664,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 43.126416666666664,
    "end": 125.83404166666665,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 43.126416666666664,
    "end": 125.83404166666665,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 43.126416666666664,
    "end": 125.83404166666665,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 125.54208333333334,
    "end": 126.126,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 125.83404166666666,
    "end": 240.53195833333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 125.83404166666666,
    "end": 240.53195833333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 125.83404166666666,
    "end": 240.53195833333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 240.24,
    "end": 240.82391666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 240.53195833333334,
    "end": 308.14116666666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 240.53195833333334,
    "end": 308.14116666666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 240.53195833333334,
    "end": 308.14116666666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 307.8492083333333,
    "end": 308.43312499999996,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 308.14116666666666,
    "end": 507.7989583333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 308.14116666666666,
    "end": 507.7989583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 308.14116666666666,
    "end": 507.7989583333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 507.507,
    "end": 508.09091666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 507.79895833333336,
    "end": 551.6344166666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 507.79895833333336,
    "end": 551.6344166666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 507.79895833333336,
    "end": 551.6344166666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 551.6344166666667,
    "end": 913.7461666666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 551.6344166666667,
    "end": 913.7461666666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 551.6344166666667,
    "end": 913.7461666666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 913.7461666666667,
    "end": 1217.7165,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 913.7461666666667,
    "end": 1217.7165,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 913.7461666666667,
    "end": 1217.7165,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1217.7165,
    "end": 1272.8549166666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1217.7165,
    "end": 1272.8549166666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1217.7165,
    "end": 1272.8549166666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1272.5629583333334,
    "end": 1273.1468750000001,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1272.8549166666667,
    "end": 1724.4310416666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1272.8549166666667,
    "end": 1724.4310416666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1272.8549166666667,
    "end": 1724.4310416666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1724.4310416666667,
    "end": 1764.2625,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1724.4310416666667,
    "end": 1764.2625,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1724.4310416666667,
    "end": 1764.2625,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1764.2625,
    "end": 1781.2377916666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1764.2625,
    "end": 1781.2377916666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1764.2625,
    "end": 1781.2377916666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1781.2377916666667,
    "end": 1904.7361666666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1781.2377916666667,
    "end": 1904.7361666666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1781.2377916666667,
    "end": 1904.7361666666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1904.4442083333333,
    "end": 1905.028125,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1904.7361666666666,
    "end": 1954.827875,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1904.7361666666666,
    "end": 1954.827875,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1904.7361666666666,
    "end": 1954.827875,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1954.827875,
    "end": 2193.065875,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1954.827875,
    "end": 2193.065875,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 1954.827875,
    "end": 2193.065875,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2193.065875,
    "end": 2221.5526666666665,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2193.065875,
    "end": 2221.5526666666665,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2193.065875,
    "end": 2221.5526666666665,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2221.5526666666665,
    "end": 2291.3724166666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2221.5526666666665,
    "end": 2291.3724166666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2221.5526666666665,
    "end": 2291.3724166666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2291.0804583333334,
    "end": 2291.664375,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2291.3724166666666,
    "end": 2311.3507083333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2291.3724166666666,
    "end": 2311.3507083333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2291.3724166666666,
    "end": 2311.3507083333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2311.05875,
    "end": 2311.6426666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2311.3507083333334,
    "end": 2417.039625,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2311.3507083333334,
    "end": 2417.039625,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2311.3507083333334,
    "end": 2417.039625,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2417.039625,
    "end": 2473.3041666666663,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2417.039625,
    "end": 2473.3041666666663,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2417.039625,
    "end": 2473.3041666666663,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2473.0122083333335,
    "end": 2473.596125,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2473.304166666667,
    "end": 2588.33575,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2473.304166666667,
    "end": 2588.33575,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2473.304166666667,
    "end": 2588.33575,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2588.0437916666665,
    "end": 2588.627708333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2588.33575,
    "end": 2737.192791666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2588.33575,
    "end": 2737.192791666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2588.33575,
    "end": 2737.192791666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2736.900833333333,
    "end": 2737.4847499999996,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2737.192791666667,
    "end": 2767.9735416666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2737.192791666667,
    "end": 2767.9735416666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2737.192791666667,
    "end": 2767.9735416666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2767.6815833333335,
    "end": 2768.2655,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2767.9735416666667,
    "end": 2822.528041666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2767.9735416666667,
    "end": 2822.528041666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2767.9735416666667,
    "end": 2822.528041666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2822.236083333333,
    "end": 2822.8199999999997,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2822.5280416666665,
    "end": 2865.2790833333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2822.5280416666665,
    "end": 2865.2790833333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2822.5280416666665,
    "end": 2865.2790833333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2864.987125,
    "end": 2865.5710416666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2865.2790833333333,
    "end": 2907.6964583333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2865.2790833333333,
    "end": 2907.6964583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2865.2790833333333,
    "end": 2907.6964583333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2907.4045,
    "end": 2907.9884166666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2907.6964583333333,
    "end": 2917.1225416666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2907.6964583333333,
    "end": 2917.1225416666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2907.6964583333333,
    "end": 2917.1225416666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2916.8305833333334,
    "end": 2917.4145,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2917.1225416666666,
    "end": 2936.9757083333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2917.1225416666666,
    "end": 2936.9757083333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2917.1225416666666,
    "end": 2936.9757083333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2936.68375,
    "end": 2937.2676666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2936.9757083333334,
    "end": 2950.6560416666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2936.9757083333334,
    "end": 2950.6560416666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2936.9757083333334,
    "end": 2950.6560416666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2950.3640833333334,
    "end": 2950.948,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2950.6560416666666,
    "end": 2962.5429166666668,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2950.6560416666666,
    "end": 2962.5429166666668,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2950.6560416666666,
    "end": 2962.5429166666668,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2962.2509583333335,
    "end": 2962.834875,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2962.5429166666668,
    "end": 3007.5462083333337,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2962.5429166666668,
    "end": 3007.5462083333337,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2962.5429166666668,
    "end": 3007.5462083333337,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3007.25425,
    "end": 3007.8381666666664,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3007.546208333333,
    "end": 3014.7200416666665,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3007.546208333333,
    "end": 3014.7200416666665,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3007.546208333333,
    "end": 3014.7200416666665,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3014.4280833333332,
    "end": 3015.0119999999997,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3014.7200416666665,
    "end": 3042.456083333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3014.7200416666665,
    "end": 3042.456083333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3014.7200416666665,
    "end": 3042.456083333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3042.164125,
    "end": 3042.7480416666663,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3042.4560833333335,
    "end": 3076.9905833333337,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3042.4560833333335,
    "end": 3076.9905833333337,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3042.4560833333335,
    "end": 3076.9905833333337,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3076.698625,
    "end": 3077.2825416666665,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3076.9905833333332,
    "end": 3093.0899999999997,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3076.9905833333332,
    "end": 3093.0899999999997,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3076.9905833333332,
    "end": 3093.0899999999997,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3092.7980416666664,
    "end": 3093.381958333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3093.09,
    "end": 3117.9064583333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3093.09,
    "end": 3117.9064583333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3093.09,
    "end": 3117.9064583333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3117.9064583333334,
    "end": 3210.1652916666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3117.9064583333334,
    "end": 3210.1652916666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3117.9064583333334,
    "end": 3210.1652916666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 3209.5396666666666,
    "end": 3210.1652916666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.07.13-khổ đau vì tiêu thụ",
    "start": 4.004,
    "end": 4.671333333333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.07.13-khổ đau vì tiêu thụ",
    "start": 4.337666666666666,
    "end": 4240.236,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.07.13-khổ đau vì tiêu thụ",
    "start": 4.337666666666666,
    "end": 4240.236,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 3.4200833333333334,
    "end": 4.045708333333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 3.75375,
    "end": 23.148125,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 3.75375,
    "end": 23.148125,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 3.75375,
    "end": 23.148125,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 22.856166666666667,
    "end": 23.440083333333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 23.148125,
    "end": 29.654625,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 23.148125,
    "end": 29.654625,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 23.148125,
    "end": 29.654625,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 29.654625,
    "end": 48.089708333333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 29.654625,
    "end": 48.089708333333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 29.654625,
    "end": 48.089708333333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 48.089708333333334,
    "end": 103.81204166666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 48.089708333333334,
    "end": 103.81204166666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 48.089708333333334,
    "end": 103.81204166666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 103.81204166666667,
    "end": 104.479375,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 103.81204166666667,
    "end": 104.479375,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 103.81204166666667,
    "end": 104.479375,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 104.479375,
    "end": 147.48066666666668,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 104.479375,
    "end": 147.48066666666668,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 104.479375,
    "end": 147.48066666666668,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 147.48066666666668,
    "end": 287.49554166666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 147.48066666666668,
    "end": 287.49554166666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 147.48066666666668,
    "end": 287.49554166666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 287.2035833333333,
    "end": 287.78749999999997,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 287.49554166666667,
    "end": 371.78808333333336,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 287.49554166666667,
    "end": 371.78808333333336,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 287.49554166666667,
    "end": 371.78808333333336,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 371.78808333333336,
    "end": 373.247875,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 371.78808333333336,
    "end": 373.247875,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 371.78808333333336,
    "end": 373.247875,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 371.78808333333336,
    "end": 373.247875,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 371.78808333333336,
    "end": 373.247875,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 371.78808333333336,
    "end": 373.247875,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 372.95591666666667,
    "end": 373.5398333333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 373.247875,
    "end": 386.260875,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 373.247875,
    "end": 386.260875,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 373.247875,
    "end": 386.260875,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 386.260875,
    "end": 403.36129166666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 386.260875,
    "end": 403.36129166666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 386.260875,
    "end": 403.36129166666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 386.260875,
    "end": 403.36129166666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 386.260875,
    "end": 403.36129166666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 386.260875,
    "end": 403.36129166666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 403.06933333333336,
    "end": 403.65325,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 403.36129166666666,
    "end": 581.7478333333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 403.36129166666666,
    "end": 581.7478333333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 403.36129166666666,
    "end": 581.7478333333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 581.7478333333333,
    "end": 640.38975,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 581.7478333333333,
    "end": 640.38975,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 581.7478333333333,
    "end": 640.38975,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 640.0977916666667,
    "end": 640.6817083333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 640.38975,
    "end": 652.526875,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 640.38975,
    "end": 652.526875,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 640.38975,
    "end": 652.526875,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 652.526875,
    "end": 658.783125,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 652.526875,
    "end": 658.783125,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 652.526875,
    "end": 658.783125,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 658.783125,
    "end": 670.544875,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 658.783125,
    "end": 670.544875,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 658.783125,
    "end": 670.544875,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 670.544875,
    "end": 678.4694583333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 670.544875,
    "end": 678.4694583333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 670.544875,
    "end": 678.4694583333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 678.4694583333334,
    "end": 731.7727083333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 678.4694583333334,
    "end": 731.7727083333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 678.4694583333334,
    "end": 731.7727083333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 731.7727083333333,
    "end": 838.4209166666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 731.7727083333333,
    "end": 838.4209166666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 731.7727083333333,
    "end": 838.4209166666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 838.4209166666667,
    "end": 881.2553750000001,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 838.4209166666667,
    "end": 881.2553750000001,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 838.4209166666667,
    "end": 881.2553750000001,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 881.255375,
    "end": 953.5359166666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 881.255375,
    "end": 953.5359166666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 881.255375,
    "end": 953.5359166666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 881.255375,
    "end": 953.5359166666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 881.255375,
    "end": 953.5359166666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 881.255375,
    "end": 953.5359166666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 953.2439583333334,
    "end": 953.8278750000001,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 953.5359166666667,
    "end": 1028.4440833333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 953.5359166666667,
    "end": 1028.4440833333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 953.5359166666667,
    "end": 1028.4440833333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1028.4440833333333,
    "end": 1221.9290416666668,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1028.4440833333333,
    "end": 1221.9290416666668,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1028.4440833333333,
    "end": 1221.9290416666668,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1221.9290416666668,
    "end": 1232.9400416666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1221.9290416666668,
    "end": 1232.9400416666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1221.9290416666668,
    "end": 1232.9400416666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1221.9290416666668,
    "end": 1232.9400416666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1221.9290416666668,
    "end": 1232.9400416666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1221.9290416666668,
    "end": 1232.9400416666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1232.9400416666667,
    "end": 1443.9842083333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1232.9400416666667,
    "end": 1443.9842083333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1232.9400416666667,
    "end": 1443.9842083333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1443.9842083333333,
    "end": 1523.4802916666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1443.9842083333333,
    "end": 1523.4802916666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1443.9842083333333,
    "end": 1523.4802916666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1523.4802916666667,
    "end": 1821.4863333333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1523.4802916666667,
    "end": 1821.4863333333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1523.4802916666667,
    "end": 1821.4863333333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1821.4863333333333,
    "end": 1887.3020833333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1821.4863333333333,
    "end": 1887.3020833333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1821.4863333333333,
    "end": 1887.3020833333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1887.3020833333333,
    "end": 2026.6913333333332,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1887.3020833333333,
    "end": 2026.6913333333332,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1887.3020833333333,
    "end": 2026.6913333333332,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2026.6913333333334,
    "end": 2121.7863333333335,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2026.6913333333334,
    "end": 2121.7863333333335,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2026.6913333333334,
    "end": 2121.7863333333335,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2121.7863333333335,
    "end": 2126.4159583333335,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2121.7863333333335,
    "end": 2126.4159583333335,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2121.7863333333335,
    "end": 2126.4159583333335,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2126.4159583333335,
    "end": 2150.3148333333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2126.4159583333335,
    "end": 2150.3148333333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2126.4159583333335,
    "end": 2150.3148333333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2150.3148333333334,
    "end": 2257.3384166666665,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2150.3148333333334,
    "end": 2257.3384166666665,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2150.3148333333334,
    "end": 2257.3384166666665,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2257.3384166666665,
    "end": 2446.485708333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2257.3384166666665,
    "end": 2446.485708333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2257.3384166666665,
    "end": 2446.485708333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2446.19375,
    "end": 2446.7776666666664,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2446.485708333333,
    "end": 2494.2417499999997,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2446.485708333333,
    "end": 2494.2417499999997,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2446.485708333333,
    "end": 2494.2417499999997,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2494.24175,
    "end": 2510.090916666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2494.24175,
    "end": 2510.090916666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2494.24175,
    "end": 2510.090916666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2510.0909166666665,
    "end": 2528.400875,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2510.0909166666665,
    "end": 2528.400875,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2510.0909166666665,
    "end": 2528.400875,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2528.400875,
    "end": 2677.2579166666665,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2528.400875,
    "end": 2677.2579166666665,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2528.400875,
    "end": 2677.2579166666665,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2676.799125,
    "end": 2677.675,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2677.2579166666665,
    "end": 2711.834125,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2677.2579166666665,
    "end": 2711.834125,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2677.2579166666665,
    "end": 2711.834125,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2711.5421666666666,
    "end": 2712.126083333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2711.834125,
    "end": 2732.2295,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2711.834125,
    "end": 2732.2295,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2711.834125,
    "end": 2732.2295,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2731.9375416666667,
    "end": 2732.521458333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2732.2295,
    "end": 2818.5657499999998,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2732.2295,
    "end": 2818.5657499999998,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2732.2295,
    "end": 2818.5657499999998,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2818.2737916666665,
    "end": 2818.857708333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2818.56575,
    "end": 2850.2223750000003,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2818.56575,
    "end": 2850.2223750000003,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2818.56575,
    "end": 2850.2223750000003,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2849.9304166666666,
    "end": 2850.514333333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2850.222375,
    "end": 3034.156125,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2850.222375,
    "end": 3034.156125,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2850.222375,
    "end": 3034.156125,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 3033.5722083333335,
    "end": 3034.156125,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 0.0,
    "end": 1.001,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 3.9622916666666668,
    "end": 4.963291666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 4.462791666666667,
    "end": 85.04329166666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 84.54279166666667,
    "end": 85.54379166666668,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 85.04329166666666,
    "end": 147.39724999999999,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 146.89675,
    "end": 147.89775,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 147.39725,
    "end": 217.75920833333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 217.25870833333335,
    "end": 218.25970833333335,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 271.145875,
    "end": 272.14687499999997,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 485.8186666666667,
    "end": 486.81966666666665,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 633.4244583333333,
    "end": 634.4254583333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 680.554875,
    "end": 681.555875,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 734.5671666666667,
    "end": 735.5681666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 766.1820833333334,
    "end": 767.1830833333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 772.1046666666666,
    "end": 773.1056666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 818.6511666666667,
    "end": 819.6521666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 888.1789583333333,
    "end": 889.1799583333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 1205.45425,
    "end": 1206.45525,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 1299.673375,
    "end": 1300.674375,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 1636.9686666666666,
    "end": 1637.9696666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 1647.5625833333334,
    "end": 1648.5635833333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 1890.5553333333332,
    "end": 1891.5563333333332,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 1903.65175,
    "end": 1904.65275,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 1926.2576666666666,
    "end": 1927.2586666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 1955.1198333333334,
    "end": 1956.1208333333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2203.7015,
    "end": 2204.7025000000003,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2282.154875,
    "end": 2283.1558750000004,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2310.05775,
    "end": 2311.05875,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2329.9109166666667,
    "end": 2330.911916666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2341.672666666667,
    "end": 2342.673666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2357.355,
    "end": 2358.356,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2372.2865833333335,
    "end": 2373.2875833333337,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2418.7496666666666,
    "end": 2419.750666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2451.073625,
    "end": 2452.074625,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2584.999083333333,
    "end": 2586.0000833333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2589.1699166666667,
    "end": 2590.170916666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2670.7097083333333,
    "end": 2671.7107083333335,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2688.143791666667,
    "end": 2689.144791666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2705.327625,
    "end": 2706.328625,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2888.5523333333335,
    "end": 2889.5533333333337,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2934.056125,
    "end": 2935.0571250000003,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 3044.041,
    "end": 3045.0420000000004,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 3088.4186666666665,
    "end": 3089.4196666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 3107.5627916666667,
    "end": 3108.563791666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 3115.9461666666666,
    "end": 3116.947166666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 3152.149,
    "end": 3153.15,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 3183.93075,
    "end": 3184.93175,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 3198.2367083333334,
    "end": 3199.2377083333336,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 3293.8322083333333,
    "end": 3294.8332083333335,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 3712.834125,
    "end": 3713.835125,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 3838.1259583333335,
    "end": 3839.1269583333337,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 3853.975125,
    "end": 3854.976125,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 3913.9934166666667,
    "end": 3914.994416666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 3914.493916666667,
    "end": 4231.644083333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 4231.1435833333335,
    "end": 4232.144583333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 4231.644083333334,
    "end": 4325.696375,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 4325.195875,
    "end": 4326.196875000001,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 4446.817375,
    "end": 4447.818375,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 4460.330875,
    "end": 4461.331875,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 4531.401875,
    "end": 4532.402875,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 4753.874125,
    "end": 4754.8751250000005,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 4801.963833333333,
    "end": 4802.964833333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 4934.846583333333,
    "end": 4935.847583333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 4935.347083333333,
    "end": 4949.736458333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 4949.235958333334,
    "end": 4950.236958333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 4949.736458333334,
    "end": 5204.240708333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 5203.2397083333335,
    "end": 5204.240708333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 0.0,
    "end": 0.6666666666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 3.7,
    "end": 4.366666666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 4.033333333333333,
    "end": 39.199999999999996,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 4.033333333333333,
    "end": 39.199999999999996,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 38.86666666666667,
    "end": 39.53333333333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 39.2,
    "end": 86.83333333333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 39.2,
    "end": 86.83333333333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 39.2,
    "end": 86.83333333333334,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 86.5,
    "end": 87.16666666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 86.83333333333333,
    "end": 123.3,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 86.83333333333333,
    "end": 123.3,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 86.83333333333333,
    "end": 123.3,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 122.96666666666667,
    "end": 123.63333333333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 123.3,
    "end": 216.36666666666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 123.3,
    "end": 216.36666666666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 123.3,
    "end": 216.36666666666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 216.03333333333333,
    "end": 216.7,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 216.36666666666667,
    "end": 329.03333333333336,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 216.36666666666667,
    "end": 329.03333333333336,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 216.36666666666667,
    "end": 329.03333333333336,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 328.7,
    "end": 329.3666666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 329.03333333333336,
    "end": 431.73333333333335,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 329.03333333333336,
    "end": 431.73333333333335,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 329.03333333333336,
    "end": 431.73333333333335,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 431.4,
    "end": 432.06666666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 431.73333333333335,
    "end": 477.03333333333336,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 431.73333333333335,
    "end": 477.03333333333336,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 431.73333333333335,
    "end": 477.03333333333336,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 476.7,
    "end": 477.3666666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 477.03333333333336,
    "end": 605.8333333333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 477.03333333333336,
    "end": 605.8333333333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 477.03333333333336,
    "end": 605.8333333333334,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 605.5,
    "end": 606.1666666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 605.8333333333334,
    "end": 616.5333333333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 605.8333333333334,
    "end": 616.5333333333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 605.8333333333334,
    "end": 616.5333333333334,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 616.2,
    "end": 616.8666666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 616.5333333333333,
    "end": 656.5,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 616.5333333333333,
    "end": 656.5,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 616.5333333333333,
    "end": 656.5,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 656.3666666666667,
    "end": 656.6333333333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 656.5,
    "end": 805.3333333333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 656.5,
    "end": 805.3333333333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 656.5,
    "end": 805.3333333333334,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 805.0,
    "end": 805.6666666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 805.3333333333334,
    "end": 1049.0333333333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 805.3333333333334,
    "end": 1049.0333333333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 805.3333333333334,
    "end": 1049.0333333333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1048.8333333333333,
    "end": 1049.1999999999998,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1049.0333333333333,
    "end": 1099.0333333333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1049.0333333333333,
    "end": 1099.0333333333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1049.0333333333333,
    "end": 1099.0333333333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1098.7,
    "end": 1099.3666666666668,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1099.0333333333333,
    "end": 1484.1666666666665,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1099.0333333333333,
    "end": 1484.1666666666665,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1099.0333333333333,
    "end": 1484.1666666666665,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1483.8333333333333,
    "end": 1484.5,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1484.1666666666667,
    "end": 1498.2,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1484.1666666666667,
    "end": 1498.2,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1484.1666666666667,
    "end": 1498.2,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1498.1333333333334,
    "end": 1498.2666666666669,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1498.2,
    "end": 1898.3666666666668,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1498.2,
    "end": 1898.3666666666668,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1498.2,
    "end": 1898.3666666666668,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1898.0333333333333,
    "end": 1898.7,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1898.3666666666666,
    "end": 1981.1999999999998,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1898.3666666666666,
    "end": 1981.1999999999998,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1898.3666666666666,
    "end": 1981.1999999999998,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1980.8666666666666,
    "end": 1981.5333333333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1981.2,
    "end": 2022.3666666666668,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1981.2,
    "end": 2022.3666666666668,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 1981.2,
    "end": 2022.3666666666668,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2022.3,
    "end": 2022.4333333333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2022.3666666666666,
    "end": 2022.7666666666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2022.3666666666666,
    "end": 2022.7666666666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2022.3666666666666,
    "end": 2022.7666666666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2022.4333333333334,
    "end": 2023.1000000000001,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2022.7666666666667,
    "end": 2051.9,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2022.7666666666667,
    "end": 2051.9,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2022.7666666666667,
    "end": 2051.9,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2051.5666666666666,
    "end": 2052.233333333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2051.9,
    "end": 2135.2333333333336,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2051.9,
    "end": 2135.2333333333336,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2051.9,
    "end": 2135.2333333333336,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2134.9,
    "end": 2135.5666666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2135.233333333333,
    "end": 2190.1666666666665,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2135.233333333333,
    "end": 2190.1666666666665,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2135.233333333333,
    "end": 2190.1666666666665,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2189.8333333333335,
    "end": 2190.5,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2190.1666666666665,
    "end": 2245.133333333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2190.1666666666665,
    "end": 2245.133333333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2190.1666666666665,
    "end": 2245.133333333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2004.09.19-đối phó với cơn bão trong lòng",
    "start": 2244.4666666666667,
    "end": 2245.133333333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 0.0,
    "end": 0.5839166666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3.75375,
    "end": 4.337666666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4.045708333333334,
    "end": 86.25283333333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4.045708333333334,
    "end": 86.25283333333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4.045708333333334,
    "end": 86.25283333333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 85.960875,
    "end": 86.54479166666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 86.25283333333333,
    "end": 229.77120833333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 86.25283333333333,
    "end": 229.77120833333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 86.25283333333333,
    "end": 229.77120833333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 229.47925,
    "end": 230.06316666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 229.77120833333333,
    "end": 253.127875,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 229.77120833333333,
    "end": 253.127875,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 229.77120833333333,
    "end": 253.127875,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 252.83591666666666,
    "end": 253.41983333333332,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 253.127875,
    "end": 448.573125,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 253.127875,
    "end": 448.573125,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 253.127875,
    "end": 448.573125,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 448.28116666666665,
    "end": 448.8650833333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 450.53341666666665,
    "end": 451.1173333333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 450.825375,
    "end": 517.0999166666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 450.825375,
    "end": 517.0999166666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 450.825375,
    "end": 517.0999166666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 516.8079583333333,
    "end": 517.391875,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 519.9777916666667,
    "end": 520.5617083333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 520.26975,
    "end": 1153.7359166666668,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 520.26975,
    "end": 1153.7359166666668,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 520.26975,
    "end": 1153.7359166666668,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1153.4439583333333,
    "end": 1154.027875,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1153.7359166666668,
    "end": 1274.7735,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1153.7359166666668,
    "end": 1274.7735,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1153.7359166666668,
    "end": 1274.7735,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1277.02575,
    "end": 1277.6096666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1277.3177083333333,
    "end": 1345.969625,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1277.3177083333333,
    "end": 1345.969625,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1277.3177083333333,
    "end": 1345.969625,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1345.6776666666667,
    "end": 1346.2615833333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1347.9299166666667,
    "end": 1348.5138333333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1348.221875,
    "end": 1361.9022083333332,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1348.221875,
    "end": 1361.9022083333332,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1348.221875,
    "end": 1361.9022083333332,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1361.61025,
    "end": 1362.1941666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1361.9022083333334,
    "end": 1406.9889166666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1361.9022083333334,
    "end": 1406.9889166666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1361.9022083333334,
    "end": 1406.9889166666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1406.6969583333334,
    "end": 1407.2808750000002,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1406.9889166666667,
    "end": 1473.8056666666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1406.9889166666667,
    "end": 1473.8056666666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1406.9889166666667,
    "end": 1473.8056666666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1473.5137083333334,
    "end": 1474.097625,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1473.8056666666666,
    "end": 1491.5317083333332,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1473.8056666666666,
    "end": 1491.5317083333332,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1473.8056666666666,
    "end": 1491.5317083333332,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1491.23975,
    "end": 1491.8236666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1493.492,
    "end": 1494.0759166666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1493.7839583333334,
    "end": 2049.8394583333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1493.7839583333334,
    "end": 2049.8394583333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 1493.7839583333334,
    "end": 2049.8394583333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2049.5475,
    "end": 2050.1314166666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2049.8394583333334,
    "end": 2130.6702083333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2049.8394583333334,
    "end": 2130.6702083333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2049.8394583333334,
    "end": 2130.6702083333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2130.37825,
    "end": 2130.9621666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2130.6702083333334,
    "end": 2172.503666666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2130.6702083333334,
    "end": 2172.503666666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2130.6702083333334,
    "end": 2172.503666666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2172.2117083333333,
    "end": 2172.7956249999997,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2174.92275,
    "end": 2175.5066666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2175.2147083333334,
    "end": 2202.7839166666668,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2175.2147083333334,
    "end": 2202.7839166666668,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2175.2147083333334,
    "end": 2202.7839166666668,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2202.4919583333335,
    "end": 2203.075875,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2205.286416666667,
    "end": 2205.8703333333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2205.578375,
    "end": 2309.0984583333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2205.578375,
    "end": 2309.0984583333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2205.578375,
    "end": 2309.0984583333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2308.8065,
    "end": 2309.3904166666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2309.0984583333334,
    "end": 2428.17575,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2309.0984583333334,
    "end": 2428.17575,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2309.0984583333334,
    "end": 2428.17575,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2427.8837916666666,
    "end": 2428.467708333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2428.17575,
    "end": 2553.968083333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2428.17575,
    "end": 2553.968083333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2428.17575,
    "end": 2553.968083333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2553.676125,
    "end": 2554.2600416666664,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2553.968083333333,
    "end": 2636.9259583333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2553.968083333333,
    "end": 2636.9259583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2553.968083333333,
    "end": 2636.9259583333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2636.634,
    "end": 2637.2179166666665,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2636.9259583333333,
    "end": 2663.077083333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2636.9259583333333,
    "end": 2663.077083333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2636.9259583333333,
    "end": 2663.077083333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2662.785125,
    "end": 2663.3690416666664,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2663.077083333333,
    "end": 2784.1563749999996,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2663.077083333333,
    "end": 2784.1563749999996,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2663.077083333333,
    "end": 2784.1563749999996,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2783.864416666667,
    "end": 2784.4483333333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2784.156375,
    "end": 2854.726875,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2784.156375,
    "end": 2854.726875,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2784.156375,
    "end": 2854.726875,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2854.4349166666666,
    "end": 2855.018833333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2858.230375,
    "end": 2858.8142916666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2858.5223333333333,
    "end": 2923.6290416666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2858.5223333333333,
    "end": 2923.6290416666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2858.5223333333333,
    "end": 2923.6290416666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2923.3370833333333,
    "end": 2923.921,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2923.6290416666666,
    "end": 3053.925875,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2923.6290416666666,
    "end": 3053.925875,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 2923.6290416666666,
    "end": 3053.925875,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3053.6339166666667,
    "end": 3054.217833333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3057.429375,
    "end": 3058.0132916666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3057.7213333333334,
    "end": 3087.209125,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3057.7213333333334,
    "end": 3087.209125,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3057.7213333333334,
    "end": 3087.209125,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3086.9171666666666,
    "end": 3087.501083333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3087.209125,
    "end": 3145.267125,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3087.209125,
    "end": 3145.267125,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3087.209125,
    "end": 3145.267125,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3149.0625833333334,
    "end": 3149.6465,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3149.3545416666666,
    "end": 3685.306625,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3149.3545416666666,
    "end": 3685.306625,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3149.3545416666666,
    "end": 3685.306625,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3685.0146666666665,
    "end": 3685.598583333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3685.306625,
    "end": 3691.1875,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3685.306625,
    "end": 3691.1875,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3685.306625,
    "end": 3691.1875,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3690.8955416666668,
    "end": 3691.4794583333332,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3691.1875,
    "end": 3792.163375,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3691.1875,
    "end": 3792.163375,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3691.1875,
    "end": 3792.163375,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3791.871416666667,
    "end": 3792.4553333333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3792.163375,
    "end": 3879.041833333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3792.163375,
    "end": 3879.041833333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3792.163375,
    "end": 3879.041833333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3878.749875,
    "end": 3879.3337916666665,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3879.041833333333,
    "end": 4076.739333333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3879.041833333333,
    "end": 4076.739333333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 3879.041833333333,
    "end": 4076.739333333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4076.447375,
    "end": 4077.0312916666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4076.7393333333334,
    "end": 4448.402291666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4076.7393333333334,
    "end": 4448.402291666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4076.7393333333334,
    "end": 4448.402291666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4448.110333333333,
    "end": 4448.69425,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4448.402291666666,
    "end": 4598.135208333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4448.402291666666,
    "end": 4598.135208333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4448.402291666666,
    "end": 4598.135208333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4597.84325,
    "end": 4598.427166666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4601.638708333333,
    "end": 4602.222624999999,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4601.930666666667,
    "end": 4793.246791666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4601.930666666667,
    "end": 4793.246791666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4601.930666666667,
    "end": 4793.246791666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4792.954833333333,
    "end": 4793.53875,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4793.2467916666665,
    "end": 4799.503041666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4793.2467916666665,
    "end": 4799.503041666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4793.2467916666665,
    "end": 4799.503041666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4799.211083333334,
    "end": 4799.795,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4799.503041666667,
    "end": 4899.728166666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4799.503041666667,
    "end": 4899.728166666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4799.503041666667,
    "end": 4899.728166666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2009.11.29-điềm lành lớn nhất",
    "start": 4899.102541666667,
    "end": 4899.728166666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 0.0,
    "end": 0.5839166666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3.7120416666666665,
    "end": 4.337666666666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 4.045708333333334,
    "end": 48.00629166666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 4.045708333333334,
    "end": 48.00629166666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 4.045708333333334,
    "end": 48.00629166666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 4.045708333333334,
    "end": 48.00629166666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 4.045708333333334,
    "end": 48.00629166666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 4.045708333333334,
    "end": 48.00629166666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 4.045708333333334,
    "end": 48.00629166666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 4.045708333333334,
    "end": 48.00629166666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 4.045708333333334,
    "end": 48.00629166666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 4.045708333333334,
    "end": 48.00629166666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 48.00629166666667,
    "end": 89.50608333333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 48.00629166666667,
    "end": 89.50608333333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 48.00629166666667,
    "end": 89.50608333333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 48.00629166666667,
    "end": 89.50608333333334,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 48.00629166666667,
    "end": 89.50608333333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 89.50608333333334,
    "end": 89.88145833333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 89.50608333333334,
    "end": 89.88145833333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 89.50608333333334,
    "end": 89.88145833333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 89.50608333333334,
    "end": 89.88145833333334,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 89.50608333333334,
    "end": 89.88145833333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 89.88145833333333,
    "end": 217.17529166666668,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 89.88145833333333,
    "end": 217.17529166666668,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 89.88145833333333,
    "end": 217.17529166666668,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 89.88145833333333,
    "end": 217.17529166666668,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 89.88145833333333,
    "end": 217.17529166666668,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 217.17529166666668,
    "end": 526.8179583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 217.17529166666668,
    "end": 526.8179583333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 217.17529166666668,
    "end": 526.8179583333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 217.17529166666668,
    "end": 526.8179583333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 217.17529166666668,
    "end": 526.8179583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 526.526,
    "end": 527.1099166666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 526.8179583333333,
    "end": 1310.4758333333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 526.8179583333333,
    "end": 1310.4758333333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 526.8179583333333,
    "end": 1310.4758333333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 526.8179583333333,
    "end": 1310.4758333333334,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 526.8179583333333,
    "end": 1310.4758333333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 1310.183875,
    "end": 1310.7677916666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 1310.4758333333334,
    "end": 1713.5034583333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 1310.4758333333334,
    "end": 1713.5034583333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 1310.4758333333334,
    "end": 1713.5034583333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 1310.4758333333334,
    "end": 1713.5034583333334,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 1310.4758333333334,
    "end": 1713.5034583333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 1713.2115,
    "end": 1713.7954166666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 1713.5034583333334,
    "end": 2493.1990416666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 1713.5034583333334,
    "end": 2493.1990416666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 1713.5034583333334,
    "end": 2493.1990416666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 1713.5034583333334,
    "end": 2493.1990416666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 1713.5034583333334,
    "end": 2493.1990416666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 2492.9070833333335,
    "end": 2493.491,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 2493.1990416666667,
    "end": 2830.3692083333335,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 2493.1990416666667,
    "end": 2830.3692083333335,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 2493.1990416666667,
    "end": 2830.3692083333335,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 2493.1990416666667,
    "end": 2830.3692083333335,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 2493.1990416666667,
    "end": 2830.3692083333335,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 2830.3692083333335,
    "end": 3045.500791666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 2830.3692083333335,
    "end": 3045.500791666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 2830.3692083333335,
    "end": 3045.500791666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 2830.3692083333335,
    "end": 3045.500791666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 2830.3692083333335,
    "end": 3045.500791666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3045.500791666667,
    "end": 3068.648916666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3045.500791666667,
    "end": 3068.648916666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3045.500791666667,
    "end": 3068.648916666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3045.500791666667,
    "end": 3068.648916666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3045.500791666667,
    "end": 3068.648916666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3068.6489166666665,
    "end": 3098.220125,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3068.6489166666665,
    "end": 3098.220125,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3068.6489166666665,
    "end": 3098.220125,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3068.6489166666665,
    "end": 3098.220125,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3068.6489166666665,
    "end": 3098.220125,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3098.220125,
    "end": 3244.6580833333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3098.220125,
    "end": 3244.6580833333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3098.220125,
    "end": 3244.6580833333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3098.220125,
    "end": 3244.6580833333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3098.220125,
    "end": 3244.6580833333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3244.366125,
    "end": 3244.9500416666665,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3244.6580833333333,
    "end": 3282.6126666666664,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3244.6580833333333,
    "end": 3282.6126666666664,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3244.6580833333333,
    "end": 3282.6126666666664,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3244.6580833333333,
    "end": 3282.6126666666664,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3244.6580833333333,
    "end": 3282.6126666666664,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3281.9870416666668,
    "end": 3282.612666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 0.0,
    "end": 0.625625,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3.2115416666666667,
    "end": 3.7954583333333334,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3.5035,
    "end": 208.49995833333332,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3.5035,
    "end": 208.49995833333332,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3.5035,
    "end": 208.49995833333332,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3.5035,
    "end": 208.49995833333332,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3.5035,
    "end": 208.49995833333332,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3.5035,
    "end": 208.49995833333332,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 208.49995833333332,
    "end": 264.51425,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 208.49995833333332,
    "end": 264.51425,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 208.49995833333332,
    "end": 264.51425,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 208.49995833333332,
    "end": 264.51425,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 208.49995833333332,
    "end": 264.51425,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 208.49995833333332,
    "end": 264.51425,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 264.22229166666665,
    "end": 264.8062083333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 264.51425,
    "end": 622.8305416666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 264.51425,
    "end": 622.8305416666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 264.51425,
    "end": 622.8305416666667,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 264.51425,
    "end": 622.8305416666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 264.51425,
    "end": 622.8305416666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 264.51425,
    "end": 622.8305416666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 622.5385833333333,
    "end": 623.1225000000001,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 622.8305416666667,
    "end": 795.7532916666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 622.8305416666667,
    "end": 795.7532916666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 622.8305416666667,
    "end": 795.7532916666667,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 622.8305416666667,
    "end": 795.7532916666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 622.8305416666667,
    "end": 795.7532916666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 622.8305416666667,
    "end": 795.7532916666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 795.4613333333333,
    "end": 796.04525,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 795.7532916666667,
    "end": 920.7114583333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 795.7532916666667,
    "end": 920.7114583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 795.7532916666667,
    "end": 920.7114583333333,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 795.7532916666667,
    "end": 920.7114583333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 795.7532916666667,
    "end": 920.7114583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 795.7532916666667,
    "end": 920.7114583333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 920.7114583333333,
    "end": 984.5252083333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 920.7114583333333,
    "end": 984.5252083333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 920.7114583333333,
    "end": 984.5252083333334,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 920.7114583333333,
    "end": 984.5252083333334,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 920.7114583333333,
    "end": 984.5252083333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 920.7114583333333,
    "end": 984.5252083333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 984.5252083333334,
    "end": 1019.3099583333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 984.5252083333334,
    "end": 1019.3099583333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 984.5252083333334,
    "end": 1019.3099583333334,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 984.5252083333334,
    "end": 1019.3099583333334,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 984.5252083333334,
    "end": 1019.3099583333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 984.5252083333334,
    "end": 1019.3099583333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1019.3099583333334,
    "end": 1033.0737083333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1019.3099583333334,
    "end": 1033.0737083333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1019.3099583333334,
    "end": 1033.0737083333333,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1019.3099583333334,
    "end": 1033.0737083333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1019.3099583333334,
    "end": 1033.0737083333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1019.3099583333334,
    "end": 1033.0737083333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1033.0737083333333,
    "end": 1048.047,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1033.0737083333333,
    "end": 1048.047,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1033.0737083333333,
    "end": 1048.047,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1033.0737083333333,
    "end": 1048.047,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1033.0737083333333,
    "end": 1048.047,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1033.0737083333333,
    "end": 1048.047,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1047.7550416666666,
    "end": 1048.3389583333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1048.047,
    "end": 1081.5805,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1048.047,
    "end": 1081.5805,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1048.047,
    "end": 1081.5805,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1048.047,
    "end": 1081.5805,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1048.047,
    "end": 1081.5805,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1048.047,
    "end": 1081.5805,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1081.2885416666666,
    "end": 1081.8724583333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1081.5805,
    "end": 1083.6242083333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1081.5805,
    "end": 1083.6242083333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1081.5805,
    "end": 1083.6242083333334,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1081.5805,
    "end": 1083.6242083333334,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1081.5805,
    "end": 1083.6242083333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1081.5805,
    "end": 1083.6242083333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1083.6242083333334,
    "end": 1136.5520833333335,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1083.6242083333334,
    "end": 1136.5520833333335,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1083.6242083333334,
    "end": 1136.5520833333335,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1083.6242083333334,
    "end": 1136.5520833333335,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1083.6242083333334,
    "end": 1136.5520833333335,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1083.6242083333334,
    "end": 1136.5520833333335,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1136.5520833333333,
    "end": 1138.3038333333332,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1136.5520833333333,
    "end": 1138.3038333333332,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1136.5520833333333,
    "end": 1138.3038333333332,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1136.5520833333333,
    "end": 1138.3038333333332,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1136.5520833333333,
    "end": 1138.3038333333332,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1136.5520833333333,
    "end": 1138.3038333333332,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1138.3038333333334,
    "end": 1592.1322083333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1138.3038333333334,
    "end": 1592.1322083333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1138.3038333333334,
    "end": 1592.1322083333334,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1138.3038333333334,
    "end": 1592.1322083333334,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1138.3038333333334,
    "end": 1592.1322083333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1138.3038333333334,
    "end": 1592.1322083333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1592.1322083333334,
    "end": 1675.2569166666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1592.1322083333334,
    "end": 1675.2569166666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1592.1322083333334,
    "end": 1675.2569166666667,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1592.1322083333334,
    "end": 1675.2569166666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1592.1322083333334,
    "end": 1675.2569166666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1592.1322083333334,
    "end": 1675.2569166666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1674.9649583333332,
    "end": 1675.548875,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1675.2569166666667,
    "end": 1741.4063333333334,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1675.2569166666667,
    "end": 1741.4063333333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1675.2569166666667,
    "end": 1741.4063333333334,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1675.2569166666667,
    "end": 1741.4063333333334,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1675.2569166666667,
    "end": 1741.4063333333334,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1675.2569166666667,
    "end": 1741.4063333333334,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1741.114375,
    "end": 1741.6982916666668,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1741.4063333333334,
    "end": 1806.8467083333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1741.4063333333334,
    "end": 1806.8467083333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1741.4063333333334,
    "end": 1806.8467083333333,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1741.4063333333334,
    "end": 1806.8467083333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1741.4063333333334,
    "end": 1806.8467083333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1741.4063333333334,
    "end": 1806.8467083333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1806.55475,
    "end": 1807.1386666666667,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1806.8467083333333,
    "end": 1963.962,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1806.8467083333333,
    "end": 1963.962,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1806.8467083333333,
    "end": 1963.962,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1806.8467083333333,
    "end": 1963.962,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1806.8467083333333,
    "end": 1963.962,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1806.8467083333333,
    "end": 1963.962,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1963.962,
    "end": 2665.329333333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1963.962,
    "end": 2665.329333333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1963.962,
    "end": 2665.329333333333,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1963.962,
    "end": 2665.329333333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1963.962,
    "end": 2665.329333333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1963.962,
    "end": 2665.329333333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2665.329333333333,
    "end": 2714.628583333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2665.329333333333,
    "end": 2714.628583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2665.329333333333,
    "end": 2714.628583333333,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2665.329333333333,
    "end": 2714.628583333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2665.329333333333,
    "end": 2714.628583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2665.329333333333,
    "end": 2714.628583333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2714.336625,
    "end": 2714.9205416666664,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2714.628583333333,
    "end": 2733.3556249999997,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2714.628583333333,
    "end": 2733.3556249999997,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2714.628583333333,
    "end": 2733.3556249999997,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2714.628583333333,
    "end": 2733.3556249999997,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2714.628583333333,
    "end": 2733.3556249999997,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2714.628583333333,
    "end": 2733.3556249999997,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2733.355625,
    "end": 2737.067666666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2733.355625,
    "end": 2737.067666666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2733.355625,
    "end": 2737.067666666667,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2733.355625,
    "end": 2737.067666666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2733.355625,
    "end": 2737.067666666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2733.355625,
    "end": 2737.067666666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2737.067666666667,
    "end": 3253.2917083333336,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2737.067666666667,
    "end": 3253.2917083333336,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2737.067666666667,
    "end": 3253.2917083333336,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2737.067666666667,
    "end": 3253.2917083333336,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2737.067666666667,
    "end": 3253.2917083333336,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2737.067666666667,
    "end": 3253.2917083333336,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3253.291708333333,
    "end": 3351.4314166666663,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3253.291708333333,
    "end": 3351.4314166666663,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3253.291708333333,
    "end": 3351.4314166666663,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3253.291708333333,
    "end": 3351.4314166666663,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3253.291708333333,
    "end": 3351.4314166666663,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3253.291708333333,
    "end": 3351.4314166666663,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3351.431416666667,
    "end": 3356.60325,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3351.431416666667,
    "end": 3356.60325,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3351.431416666667,
    "end": 3356.60325,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3351.431416666667,
    "end": 3356.60325,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3351.431416666667,
    "end": 3356.60325,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3351.431416666667,
    "end": 3356.60325,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3356.60325,
    "end": 3357.4791250000003,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3356.60325,
    "end": 3357.4791250000003,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3356.60325,
    "end": 3357.4791250000003,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3356.60325,
    "end": 3357.4791250000003,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3356.60325,
    "end": 3357.4791250000003,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3356.60325,
    "end": 3357.4791250000003,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3357.479125,
    "end": 3361.2328749999997,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3357.479125,
    "end": 3361.2328749999997,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3357.479125,
    "end": 3361.2328749999997,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3357.479125,
    "end": 3361.2328749999997,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3357.479125,
    "end": 3361.2328749999997,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3357.479125,
    "end": 3361.2328749999997,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3361.232875,
    "end": 3372.8277916666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3361.232875,
    "end": 3372.8277916666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3361.232875,
    "end": 3372.8277916666666,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3361.232875,
    "end": 3372.8277916666666,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3361.232875,
    "end": 3372.8277916666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3361.232875,
    "end": 3372.8277916666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3372.8277916666666,
    "end": 3373.661958333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3372.8277916666666,
    "end": 3373.661958333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3372.8277916666666,
    "end": 3373.661958333333,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3372.8277916666666,
    "end": 3373.661958333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3372.8277916666666,
    "end": 3373.661958333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3372.8277916666666,
    "end": 3373.661958333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3373.661958333333,
    "end": 3387.7176666666664,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3373.661958333333,
    "end": 3387.7176666666664,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3373.661958333333,
    "end": 3387.7176666666664,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3373.661958333333,
    "end": 3387.7176666666664,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3373.661958333333,
    "end": 3387.7176666666664,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3373.661958333333,
    "end": 3387.7176666666664,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3387.7176666666664,
    "end": 3389.302583333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3387.7176666666664,
    "end": 3389.302583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3387.7176666666664,
    "end": 3389.302583333333,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3387.7176666666664,
    "end": 3389.302583333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3387.7176666666664,
    "end": 3389.302583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3387.7176666666664,
    "end": 3389.302583333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3389.302583333333,
    "end": 3391.8467916666664,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3389.302583333333,
    "end": 3391.8467916666664,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3389.302583333333,
    "end": 3391.8467916666664,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3389.302583333333,
    "end": 3391.8467916666664,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3389.302583333333,
    "end": 3391.8467916666664,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3389.302583333333,
    "end": 3391.8467916666664,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3391.846791666667,
    "end": 3394.766375,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3391.846791666667,
    "end": 3394.766375,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3391.846791666667,
    "end": 3394.766375,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3391.846791666667,
    "end": 3394.766375,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3391.846791666667,
    "end": 3394.766375,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3391.846791666667,
    "end": 3394.766375,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3394.766375,
    "end": 3401.481416666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3394.766375,
    "end": 3401.481416666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3394.766375,
    "end": 3401.481416666667,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3394.766375,
    "end": 3401.481416666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3394.766375,
    "end": 3401.481416666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3394.766375,
    "end": 3401.481416666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3401.4814166666665,
    "end": 3404.401,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3401.4814166666665,
    "end": 3404.401,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3401.4814166666665,
    "end": 3404.401,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3401.4814166666665,
    "end": 3404.401,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3401.4814166666665,
    "end": 3404.401,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3401.4814166666665,
    "end": 3404.401,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3404.401,
    "end": 3433.68025,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3404.401,
    "end": 3433.68025,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3404.401,
    "end": 3433.68025,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3404.401,
    "end": 3433.68025,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3404.401,
    "end": 3433.68025,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3404.401,
    "end": 3433.68025,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3433.3882916666666,
    "end": 3433.972208333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3433.68025,
    "end": 3607.520583333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3433.68025,
    "end": 3607.520583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3433.68025,
    "end": 3607.520583333333,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3433.68025,
    "end": 3607.520583333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3433.68025,
    "end": 3607.520583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3433.68025,
    "end": 3607.520583333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3607.5205833333334,
    "end": 3621.5345833333336,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3607.5205833333334,
    "end": 3621.5345833333336,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3607.5205833333334,
    "end": 3621.5345833333336,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3607.5205833333334,
    "end": 3621.5345833333336,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3607.5205833333334,
    "end": 3621.5345833333336,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3607.5205833333334,
    "end": 3621.5345833333336,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3621.5345833333336,
    "end": 3681.9699583333336,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3621.5345833333336,
    "end": 3681.9699583333336,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3621.5345833333336,
    "end": 3681.9699583333336,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3621.5345833333336,
    "end": 3681.9699583333336,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3621.5345833333336,
    "end": 3681.9699583333336,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3621.5345833333336,
    "end": 3681.9699583333336,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3681.969958333333,
    "end": 3693.7734166666664,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3681.969958333333,
    "end": 3693.7734166666664,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3681.969958333333,
    "end": 3693.7734166666664,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3681.969958333333,
    "end": 3693.7734166666664,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3681.969958333333,
    "end": 3693.7734166666664,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3681.969958333333,
    "end": 3693.7734166666664,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3693.773416666667,
    "end": 3713.71,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3693.773416666667,
    "end": 3713.71,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3693.773416666667,
    "end": 3713.71,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3693.773416666667,
    "end": 3713.71,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3693.773416666667,
    "end": 3713.71,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3693.773416666667,
    "end": 3713.71,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3713.71,
    "end": 3957.9122916666665,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3713.71,
    "end": 3957.9122916666665,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3713.71,
    "end": 3957.9122916666665,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3713.71,
    "end": 3957.9122916666665,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3713.71,
    "end": 3957.9122916666665,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3713.71,
    "end": 3957.9122916666665,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3957.9122916666665,
    "end": 3971.884583333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3957.9122916666665,
    "end": 3971.884583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3957.9122916666665,
    "end": 3971.884583333333,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3957.9122916666665,
    "end": 3971.884583333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3957.9122916666665,
    "end": 3971.884583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3957.9122916666665,
    "end": 3971.884583333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3971.8845833333335,
    "end": 4085.7066250000003,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3971.8845833333335,
    "end": 4085.7066250000003,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3971.8845833333335,
    "end": 4085.7066250000003,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3971.8845833333335,
    "end": 4085.7066250000003,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3971.8845833333335,
    "end": 4085.7066250000003,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3971.8845833333335,
    "end": 4085.7066250000003,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4085.4146666666666,
    "end": 4085.998583333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4085.706625,
    "end": 4116.028583333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4085.706625,
    "end": 4116.028583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4085.706625,
    "end": 4116.028583333333,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4085.706625,
    "end": 4116.028583333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4085.706625,
    "end": 4116.028583333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4085.706625,
    "end": 4116.028583333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4115.736625,
    "end": 4116.320541666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4116.028583333334,
    "end": 4139.260125000001,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4116.028583333334,
    "end": 4139.260125000001,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4116.028583333334,
    "end": 4139.260125000001,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4116.028583333334,
    "end": 4139.260125000001,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4116.028583333334,
    "end": 4139.260125000001,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4116.028583333334,
    "end": 4139.260125000001,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4139.260125,
    "end": 4139.760625,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4139.260125,
    "end": 4139.760625,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4139.260125,
    "end": 4139.760625,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4139.260125,
    "end": 4139.760625,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4139.260125,
    "end": 4139.760625,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4139.260125,
    "end": 4139.760625,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4139.760625,
    "end": 4277.481541666666,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4139.760625,
    "end": 4277.481541666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4139.760625,
    "end": 4277.481541666666,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4139.760625,
    "end": 4277.481541666666,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4139.760625,
    "end": 4277.481541666666,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4139.760625,
    "end": 4277.481541666666,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4277.481541666667,
    "end": 4313.767791666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4277.481541666667,
    "end": 4313.767791666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4277.481541666667,
    "end": 4313.767791666667,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4277.481541666667,
    "end": 4313.767791666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4277.481541666667,
    "end": 4313.767791666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4277.481541666667,
    "end": 4313.767791666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4313.767791666667,
    "end": 4320.316000000001,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4313.767791666667,
    "end": 4320.316000000001,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4313.767791666667,
    "end": 4320.316000000001,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4313.767791666667,
    "end": 4320.316000000001,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4313.767791666667,
    "end": 4320.316000000001,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4313.767791666667,
    "end": 4320.316000000001,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4320.024041666667,
    "end": 4320.607958333333,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4320.316,
    "end": 4418.539125,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4320.316,
    "end": 4418.539125,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4320.316,
    "end": 4418.539125,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4320.316,
    "end": 4418.539125,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4320.316,
    "end": 4418.539125,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4320.316,
    "end": 4418.539125,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4418.539125,
    "end": 4442.3128750000005,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4418.539125,
    "end": 4442.3128750000005,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4418.539125,
    "end": 4442.3128750000005,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4418.539125,
    "end": 4442.3128750000005,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4418.539125,
    "end": 4442.3128750000005,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4418.539125,
    "end": 4442.3128750000005,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4442.312875,
    "end": 4474.553416666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4442.312875,
    "end": 4474.553416666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4442.312875,
    "end": 4474.553416666667,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4442.312875,
    "end": 4474.553416666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4442.312875,
    "end": 4474.553416666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4442.312875,
    "end": 4474.553416666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4474.553416666667,
    "end": 4521.225041666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4474.553416666667,
    "end": 4521.225041666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4474.553416666667,
    "end": 4521.225041666667,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4474.553416666667,
    "end": 4521.225041666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4474.553416666667,
    "end": 4521.225041666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4474.553416666667,
    "end": 4521.225041666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4521.225041666667,
    "end": 4527.314458333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4521.225041666667,
    "end": 4527.314458333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4521.225041666667,
    "end": 4527.314458333333,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4521.225041666667,
    "end": 4527.314458333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4521.225041666667,
    "end": 4527.314458333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4521.225041666667,
    "end": 4527.314458333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4527.314458333333,
    "end": 4567.104208333333,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4527.314458333333,
    "end": 4567.104208333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4527.314458333333,
    "end": 4567.104208333333,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4527.314458333333,
    "end": 4567.104208333333,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4527.314458333333,
    "end": 4567.104208333333,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4527.314458333333,
    "end": 4567.104208333333,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4566.81225,
    "end": 4567.396166666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4567.104208333333,
    "end": 4654.65,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4567.104208333333,
    "end": 4654.65,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4567.104208333333,
    "end": 4654.65,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4567.104208333333,
    "end": 4654.65,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4567.104208333333,
    "end": 4654.65,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4567.104208333333,
    "end": 4654.65,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4654.65,
    "end": 4734.2294999999995,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4654.65,
    "end": 4734.2294999999995,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4654.65,
    "end": 4734.2294999999995,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4654.65,
    "end": 4734.2294999999995,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4654.65,
    "end": 4734.2294999999995,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4654.65,
    "end": 4734.2294999999995,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4734.2295,
    "end": 4770.098666666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4734.2295,
    "end": 4770.098666666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4734.2295,
    "end": 4770.098666666667,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4734.2295,
    "end": 4770.098666666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4734.2295,
    "end": 4770.098666666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4734.2295,
    "end": 4770.098666666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4769.8067083333335,
    "end": 4770.390625,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4770.098666666667,
    "end": 4774.227791666667,
    "type": "audio_filter",
    "details": {
      "name": "Compressor"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4770.098666666667,
    "end": 4774.227791666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4770.098666666667,
    "end": 4774.227791666667,
    "type": "audio_filter",
    "details": {
      "name": "DeEsser 2"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4770.098666666667,
    "end": 4774.227791666667,
    "type": "audio_filter",
    "details": {
      "name": "Rumble Reducer"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4770.098666666667,
    "end": 4774.227791666667,
    "type": "audio_filter",
    "details": {
      "name": "Channel EQ"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4770.098666666667,
    "end": 4774.227791666667,
    "type": "audio_filter",
    "details": {
      "name": "Gain"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4773.643875,
    "end": 4774.227791666666,
    "type": "audio_filter",
    "details": {
      "name": "Audio Crossfade"
    }
  }
]
  ```
### 3.2. fadein
- **Tần suất:** Xuất hiện **8** lần trong **3/9** file.
- **Thời lượng trung bình:** 0.05 giây.
- **Ví dụ (từ `2001.08.07-sống hạnh phúc chết bình an`):**
  ```json
  [
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 881.255375,
    "end": 881.2737930555555,
    "type": "fadein",
    "details": {
      "type": "easeIn",
      "duration": "13261/720000s"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 881.255375,
    "end": 881.2886152777777,
    "type": "fadein",
    "details": {
      "type": "easeIn",
      "duration": "23933/720000s"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2026.6913333333334,
    "end": 2026.7913333333333,
    "type": "fadein",
    "details": {
      "type": "easeInOut",
      "duration": "4410/44100s"
    }
  },
  {
    "session_id": "2003.04.03-tình yêu chân thật",
    "start": 2372.787083333333,
    "end": 2372.795975,
    "type": "fadein",
    "details": {
      "type": "easeIn",
      "duration": "6402/720000s"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 2733.355625,
    "end": 2733.392688888889,
    "type": "fadein",
    "details": {
      "type": "easeIn",
      "duration": "26686/720000s"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3607.5205833333334,
    "end": 3607.5914527777777,
    "type": "fadein",
    "details": {
      "type": "easeIn",
      "duration": "51026/720000s"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3713.71,
    "end": 3713.7792027777778,
    "type": "fadein",
    "details": {
      "type": "easeIn",
      "duration": "49826/720000s"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 4474.553416666667,
    "end": 4474.615813888889,
    "type": "fadein",
    "details": {
      "type": "easeIn",
      "duration": "44926/720000s"
    }
  }
]
  ```
### 3.3. fadeout
- **Tần suất:** Xuất hiện **15** lần trong **5/9** file.
- **Thời lượng trung bình:** 0.05 giây.
- **Ví dụ (từ `1992.11.22-giác ngộ có sẵn trong ta`):**
  ```json
  [
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
    "session_id": "2000.03.19-trí tuệ là sự nghiệp lớn nhất",
    "start": 2416.94385,
    "end": 2417.039625,
    "type": "fadeout",
    "details": {
      "type": "easeIn",
      "duration": "68958/720000s"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 731.7005625,
    "end": 731.7727083333334,
    "type": "fadeout",
    "details": {
      "type": "easeIn",
      "duration": "51945/720000s"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1443.946061111111,
    "end": 1443.9842083333333,
    "type": "fadeout",
    "details": {
      "type": "easeIn",
      "duration": "27466/720000s"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1523.4259666666667,
    "end": 1523.4802916666667,
    "type": "fadeout",
    "details": {
      "type": "easeIn",
      "duration": "39114/720000s"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 1821.4579083333333,
    "end": 1821.4863333333333,
    "type": "fadeout",
    "details": {
      "type": "easeIn",
      "duration": "20466/720000s"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2026.5913333333333,
    "end": 2026.6913333333332,
    "type": "fadeout",
    "details": {
      "type": "easeInOut",
      "duration": "4410/44100s"
    }
  },
  {
    "session_id": "2001.08.07-sống hạnh phúc chết bình an",
    "start": 2850.2023513888894,
    "end": 2850.2223750000003,
    "type": "fadeout",
    "details": {
      "type": "easeIn",
      "duration": "14417/720000s"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3045.465138888889,
    "end": 3045.500791666667,
    "type": "fadeout",
    "details": {
      "type": "easeIn",
      "duration": "25670/720000s"
    }
  },
  {
    "session_id": "2012.02.19-linh đan đổi cốt mới ra về",
    "start": 3068.6025000000004,
    "end": 3068.648916666667,
    "type": "fadeout",
    "details": {
      "type": "easeIn",
      "duration": "33420/720000s"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 984.4652777777778,
    "end": 984.5252083333334,
    "type": "fadeout",
    "details": {
      "type": "easeIn",
      "duration": "43150/720000s"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 1033.0235138888888,
    "end": 1033.0737083333333,
    "type": "fadeout",
    "details": {
      "type": "easeIn",
      "duration": "36140/720000s"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3373.589255555555,
    "end": 3373.661958333333,
    "type": "fadeout",
    "details": {
      "type": "easeIn",
      "duration": "52346/720000s"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3693.743933333333,
    "end": 3693.7734166666664,
    "type": "fadeout",
    "details": {
      "type": "easeIn",
      "duration": "21228/720000s"
    }
  },
  {
    "session_id": "2014.07.29-hãy thương nhau đi",
    "start": 3713.661888888889,
    "end": 3713.71,
    "type": "fadeout",
    "details": {
      "type": "easeIn",
      "duration": "34640/720000s"
    }
  }
]
  ```
