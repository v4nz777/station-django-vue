export const toTitleCase = (str:string, isBrand:boolean=false)=> {
    let result:string;
    if(str.length <= 3 && !isBrand) result = str[0].toUpperCase()+str.slice(1)
    else if(str.length <= 3 && isBrand) result = str.toUpperCase()
    else if(str.length > 3) result = str[0].toUpperCase()+str.slice(1)
    else result = str[0].toUpperCase()+str.slice(1)
    return result
}

export const titleCaseSentence = (str:string)=> {
    let sentence = str.split(" ");
    for(let i=0;i < sentence.length;i++){
        sentence[i] = toTitleCase(sentence[i],false)
    }
    return sentence?.join(" ")
}