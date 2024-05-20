
// sec to 11:25
function secToHHMMSS(sec){
    const mm =Math.floor(sec/60)
    sec = sec %60
return mm +':' + sec

}

export default {
    secToHHMMSS
}