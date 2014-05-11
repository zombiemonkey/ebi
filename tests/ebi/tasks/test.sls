/tmp/file_{{ grains['somevalue'] }}:
  file.touch

/tmp/file_{{ pillar['what'] }}:
  file.touch
