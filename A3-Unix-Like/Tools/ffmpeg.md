- 转换格式：`ffmpeg -i input.mp4 -qscale 0 output.avi` 
- 不降低视频质量：`-qscale 0` 
- 横向/纵向拼接：`-filter_complex hstack/vstack`
- 裁减视频：
  - `ffmpeg -ss 00:30:00 -i vid.mp4 -t 60 -c copy out.mp4`
  - `ffmpeg -ss 00:30:00 -i vid.mp4 -to 00:31:00 -c copy out.mp4`

