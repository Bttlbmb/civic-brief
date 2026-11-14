"""Offline map from licensed BKG boundaries and original story illustrations."""
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]/'docs/assets'
def write(name,s): (OUT/name).write_text(s,encoding="utf-8")
def svg(w,h,s): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="none">{s}</svg>'
def map_art(place):
    import json
    from html import escape
    data=json.loads((OUT.parents[1]/'data/boundaries.json').read_text(encoding="utf-8"))
    chosen={'bobingen':'09772125','augsburg':'09761000'}[place]
    base='<rect width="540" height="250" fill="#dce5d3"/>'
    for row in data['municipalities']:
        ags=row['municipal_code']
        tone='#bed0b7' if ags.startswith('09772') else '#dfe6d7'
        if ags in ('09772125','09761000'):
            tone='#6f987b' if ags==chosen else '#a8c1ad'
        base+=f'<path d="{escape(row["path"])}" fill-rule="evenodd" fill="{tone}" stroke="#e7ecdf" stroke-width="1.1"/>'
    for row in data['municipalities']:
        if row['municipal_code']==chosen:
            base+=f'<path d="{escape(row["path"])}" fill="none" stroke="#416f50" stroke-width="1.3"/>'
    for name,x,y in [('Augsburg',294,75),('Bobingen',250,201)]:
        active=(name.lower()==place);fill='#164e39' if active else '#e9efdf';text='#fff' if active else '#385640'
        base+=f'<circle cx="{x}" cy="{y}" r="5" fill="#285e43" stroke="#f1f3e7" stroke-width="2"/><rect x="{x+11}" y="{y-11}" width="86" height="22" rx="3" fill="{fill}"/><text x="{x+54}" y="{y+4}" text-anchor="middle" font-family="Arial,sans-serif" letter-spacing="1.2" font-weight="700" font-size="11" fill="{text}">{name.upper()}</text>'
    return svg(540,250,base)
for town in ('bobingen','augsburg'):
    write(town+'.svg',map_art(town))
def scene(kind):
    # Monochrome linocut-style spot illustrations, drawn in a 300 x 190 frame.
    s='<defs><pattern id="h" width="5" height="5" patternUnits="userSpaceOnUse"><path d="M-1 6 6 -1" stroke="#9ba98f" stroke-width="1"/></pattern></defs>'
    for x,y,r in [(184,90,57),(183,91,69),(183,90,82)]:
        s+=f'<circle cx="{x}" cy="{y}" r="{r}" stroke="#becab3" stroke-dasharray="2 5"/>'
    s+='<circle cx="190" cy="54" r="22" fill="#ddba70"/><g stroke="#446448" stroke-width="2.1" stroke-linejoin="round" stroke-linecap="round">'
    def poly(p,c): return f'<polygon points="{p}" fill="{c}"/>'
    def house(x,y,w,h,d,solar):
        c='<g transform="translate(%s %s)">'%(x,y)
        c+=poly(f'0,0 {w},-{w*.21} {w},{h-w*.21} 0,{h}', '#eceddb')
        c+=poly(f'{w},-{w*.21} {w+d},-{w*.21+d*.65} {w+d},{h-w*.21-d*.65} {w},{h-w*.21}', 'url(#h)')
        c+=poly(f'-3,1 {d*.5},-{d} {w+d*.5},-{d+w*.21} {w+2},-{w*.21}', '#8eab8c')
        c+=poly(f'{w+2},-{w*.21} {w+d*.5},-{d+w*.21} {w+d+2},-{w*.21+d*.65}', '#d1d7bf')
        if solar:
            for i in range(5):
                for j in range(2):
                    u=d*.12+j*d*.18; a=8+i*(w-12)/5+u*.42; b=-a*.21-u
                    c+=poly(f'{a},{b} {a+10},{b-2.1} {a+13},{b-7.1} {a+3},{b-5}', '#406653')
        for i in range(int(w//17)):
            a=6+i*17;b=7-a*.21
            c+=poly(f'{a},{b} {a+7},{b-1.5} {a+7},{b+8} {a},{b+9.5}', '#99ad96')
        return c+'</g>'
    def tree(x,y,z):
        return f'<g transform="translate({x} {y}) scale({z})"><path d="M0 0v-33"/><path d="M-2 -15C-13 -12 -18 -23 -13 -31 -18 -41 -12 -48 -6 -48 -1 -61 10 -54 11 -46 22 -44 20 -32 17 -29 20 -16 9 -12 3 -16Z" fill="#b9c8a8"/><path d="M1 -9v-24m0 10 8 -8m-8 1 -6 -6"/></g>'
    s+='<path d="m22 150 157 -35 108 23 -162 42Z" fill="#d7ddc6" stroke="none"/><path d="m33 156 92 22 162 -39m-237 23 74 18 106 -25" stroke="#a7b69e"/>'
    s+=tree(69,112,.68)+tree(237,104,.81)+house(110,109,73,23,27,True)+house(64,135,78,24,33,True)+tree(222,140,.65)+tree(202,150,.44)
    if kind=='augsburg':
        s='<circle cx="195" cy="49" r="23" fill="#dfc585"/><g stroke-linecap="round" stroke-linejoin="round" stroke="#49694e" stroke-width="2"><path fill="#d7e0c9" stroke="none" d="m15 137 93-32 174 19-95 53z"/><path fill="#9ebfb5" d="M13 129c44 10 33 10 62 31s69 18 104-3 55-20 102-14l-4 11c-40-5-53-9-91 14s-88 25-124-1-31-22-51-25"/><path d="M70 155q46 42 113 1m-36 16 16-6" fill="none" stroke="#e2ece0"/>'+house(111,102,84,33,26,False)+'<path fill="#b8c4aa" d="M87 117V65l13 1 3 48zm33-19 2-65h9l3 63z"/><path fill="#ebeddb" d="m78 116 14-13v8l14-14v9l14-14v12l12-11 14 6v32l-68 17z"/><path fill="#8da68d" d="m145 100 12-8v29l-12 10z"/><path d="M87 123v7m13-10v7m13-10v7m13-10v7m-4-86h10"/><path d="M117 148q18-3 30-10m-63 17 15 3" stroke="#789582"/>'+tree(233,126,.73)+tree(249,131,.57)

    return svg(300,190,s+'</g>')
for place in ['bobingen','augsburg']: write(place+'-story.svg',scene(place))
