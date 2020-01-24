def recupConstantesDES(clefs):
    f=open("ConstantesDES.txt", "r")
    txt=f.read()
    sdl='\n'
    X=dict()
    for clef in clefs:
        deb=txt.find(clef+' =')
        fin=txt.find('FIN '+clef)
        source= ""
        while(txt[deb]!=sdl and deb<fin):
            deb+=1
        deb+=1
        while(deb<fin):
            if(txt[deb] != sdl):
                source += txt[deb]
            else:
                source += '\t'
            deb += 1
        result = dict()
        string_splited = source[:-1].split("\t")
        for i in range(len(string_splited)):
            result[i] = string_splited[i]
        X[clef] = result
    return(X)
