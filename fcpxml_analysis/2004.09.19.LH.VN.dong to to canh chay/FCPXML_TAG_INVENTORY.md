# FCPXML Tag Inventory: `2004.09.19.LH.VN.dong to to canh chay.fcpxml`
This report lists all unique XML tags found in the specified FCPXML file.
*Báo cáo này liệt kê tất cả các thẻ XML duy nhất được tìm thấy trong file FCPXML được chỉ định.*

| Tag Name / Tên Thẻ | Type / Phân Loại | Description / Mô tả | Count / Số lần XH | Example Attributes / Ví dụ Thuộc tính |
| :--- | :--- | :--- | :--- | :--- |
| `adjust-noiseReduction` | **Audio Adjustment** | Hiệu ứng giảm nhiễu nền cụ thể. | 15 | `amount="50"` |
| `adjust-transform` | **Video Adjustment** | Điều chỉnh vị trí, kích thước, xoay hình ảnh. | 23 | `position="-1.03358 -8.90001" scale="1.37261 1.37261"` |
| `adjust-volume` | **Audio Adjustment** | Điều chỉnh âm lượng tổng thể của clip. | 23 | `` |
| `array` | **Unknown** | Thẻ chưa được định nghĩa trong bộ quy tắc. | 1 | `` |
| `asset` | **Core Structure** | Định nghĩa một file media (video, audio, image). | 2 | `id="r4" name="LoGo LM" uid="5B9BC57BCF264194CA75BB4348B8663E" start="0s" duration="0s" hasVideo="1" format="r5" videoSources="1"` |
| `asset-clip` | **Clip Type** | Clip cơ bản, trỏ đến file media gốc. Cốt lõi của Time Map. | 23 | `ref="r6" offset="12100/3000s" name="2004.09.19.LH.VN.dong to to canh chay" start="221000/3000s" duration="105500/3000s" tcFormat="NDF" audioRole="dialogue"` |
| `audio-channel-source` | **Audio Adjustment** | Lựa chọn kênh audio (L/R/Stereo). | 23 | `srcCh="1, 2" role="dialogue.dialogue-1"` |
| `bookmark` | **Unknown** | Thẻ chưa được định nghĩa trong bộ quy tắc. | 2 | `` |
| `caption` | **Metadata** | Phụ đề được nhúng. | 6 | `lane="1" offset="1321000/3000s" name="tới những người nghe tụng" start="10808300/3000s" duration="10900/3000s" role="iTT?captionFormat=ITT.en"` |
| `data` | **Unknown** | Thẻ chưa được định nghĩa trong bộ quy tắc. | 94 | `key="effectConfig"` |
| `effect` | **Detailed Parameter** | Định nghĩa một hiệu ứng cụ thể, là thẻ con của <filter-audio>. | 7 | `id="r2" name="Cross Dissolve" uid="FxPlug:4731E73A-8DAC-4113-9A30-AE85B1761265"` |
| `event` | **Core Structure** | Một sự kiện, chứa các project và clip. | 1 | `name="2004.09.19.LH.VN.dong to to canh chay" uid="A1327D20-A013-4E7B-9655-7105ACE05B0E"` |
| `fcpxml` | **Core Structure** | Thẻ gốc của tài liệu. | 1 | `version="1.12"` |
| `filter-audio` | **Audio Adjustment** | Áp dụng một hiệu ứng âm thanh. | 93 | `ref="r3" name="Audio Crossfade"` |
| `filter-video` | **Video Adjustment** | Áp dụng bộ lọc màu, hiệu ứng hình ảnh. | 71 | `ref="r2" name="Cross Dissolve"` |
| `format` | **Core Structure** | Định nghĩa một định dạng video (độ phân giải, frame rate). | 2 | `id="r1" name="FFVideoFormat720p30" frameDuration="100/3000s" width="1280" height="720" colorSpace="1-1-1 (Rec. 709)"` |
| `keyframe` | **Detailed Parameter** | Một điểm neo thời gian cho animation (ví dụ: âm lượng giảm dần). | 289067 | `time="56400000/720000s" value="-96dB"` |
| `keyframeAnimation` | **Detailed Parameter** | Chứa một chuỗi các keyframe. | 23 | `` |
| `library` | **Core Structure** | Thư viện chứa các event và project. | 1 | `location="file:///Users/Hoang/Movies/2004.09.19.LH.VN.dong%20to%20to%20canh%20chay.fcpbundle/"` |
| `match-clip` | **Unknown** | Thẻ chưa được định nghĩa trong bộ quy tắc. | 1 | `rule="is" type="project"` |
| `match-media` | **Unknown** | Thẻ chưa được định nghĩa trong bộ quy tắc. | 4 | `rule="is" type="videoOnly"` |
| `match-ratings` | **Unknown** | Thẻ chưa được định nghĩa trong bộ quy tắc. | 1 | `value="favorites"` |
| `md` | **Metadata** | Một cặp key-value metadata. | 11 | `key="com.apple.proapps.studio.rawToLogConversion" value="0"` |
| `media-rep` | **Unknown** | Thẻ chưa được định nghĩa trong bộ quy tắc. | 2 | `kind="original-media" sig="5B9BC57BCF264194CA75BB4348B8663E" src="file:///Volumes/P%20Co%CC%82ng%202T%20SSD/2004.09.19.LH.VN.dong%20to%20to%20canh%20chay/LoGo%20LM.png"` |
| `metadata` | **Metadata** | Chứa các thẻ metadata con. | 2 | `` |
| `param` | **Detailed Parameter** | Một tham số của effect, ví dụ: 'gain', 'frequency'. | 504 | `name="Look" key="1" value="11 (Video)"` |
| `project` | **Core Structure** | Một project, chứa timeline chính. | 1 | `name="2004.09.19.LH.VN.dong to to canh chay" uid="BA44EC4A-BDE1-4865-BB36-D0877FC7329F" modDate="2024-08-08 07:26:19 +0700"` |
| `resources` | **Core Structure** | Khai báo tất cả các tài nguyên (assets, formats). | 1 | `` |
| `sequence` | **Core Structure** | Timeline chính của project. | 1 | `format="r1" duration="6735400/3000s" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k"` |
| `smart-collection` | **Unknown** | Thẻ chưa được định nghĩa trong bộ quy tắc. | 5 | `name="Projects" match="all"` |
| `spine` | **Core Structure** | Trục chính của timeline, chứa các clip. | 1 | `` |
| `string` | **Unknown** | Thẻ chưa được định nghĩa trong bộ quy tắc. | 2 | `` |
| `text` | **Metadata** | Một lớp văn bản trên video. | 6 | `placement="bottom"` |
| `text-style` | **Unknown** | Thẻ chưa được định nghĩa trong bộ quy tắc. | 12 | `ref="ts1"` |
| `text-style-def` | **Unknown** | Thẻ chưa được định nghĩa trong bộ quy tắc. | 6 | `id="ts1"` |
| `transition` | **Video Adjustment** | Hiệu ứng chuyển cảnh. | 25 | `name="Cross Dissolve" offset="0s" duration="2000/3000s"` |
| `video` | **Video Adjustment** | Chứa các thông tin và hiệu ứng liên quan đến track video. | 1 | `ref="r4" offset="0s" name="Logo LM" start="10803100/3000s" duration="12100/3000s"` |