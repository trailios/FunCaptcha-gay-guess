import json
import string, execjs


def flagged(data: list) -> bool:
    if not data or not isinstance(data, list):
        return False
    values = [value for d in data for value in d.values()]
    if not values:
        return False

    def ends_with_uppercase(value):
        return value and value[-1] in string.ascii_uppercase

    return all(ends_with_uppercase(value) for value in values)


def pguesses(guesses: list, token: str) -> list:
    sess: str
    ion: str

    sess, ion = token.split(".")
    answers: list = []

    for guess in guesses:
        if "index" in guess:
            answers.append({"index": guess["index"], sess: ion})
        else:
            guess: dict = json.loads(guess)
            answers.append(
                {
                    "px": guess["px"],
                    "py": guess["py"],
                    "x": guess["x"],
                    "y": guess["y"],
                    sess: ion,
                }
            )

    return answers


def process(dapib_code: str, answers: list) -> list:
    ctx = execjs.compile(
        """
    function runCode(dapibCode, answers) {
        window = {};
        window.parent = {};
        window.parent.ae = {"answer": answers};
        window.parent.ae["dapibRecei" + "ve"] = function(data) {
            response = JSON.stringify(data);
        };
        
        eval(dapibCode);
        return response;
    }
    """
    )

    result: str = ctx.call("runCode", dapib_code, answers)
    result: dict = json.loads(result)

    if flagged(result["tanswer"]):
        for array in result["tanswer"]:
            for item in array:
                array[item] = (
                    array[item][:-1] if isinstance(array[item], str) else array[item]
                )

    return result["tanswer"]


def main(dapib_code: str, token: str, guesses: list) -> list:
    answers: list = pguesses(guesses, token)
    result: list = process(dapib_code, answers)

    return result


if __name__ == "__main__":
    testcode: str = "(function(){const i={'FvzKH':function(p,a){return p*a;},'LyKKG':function(p,a){return p%a;},'QDvZR':function(p,a){return p+a;},'kWbTh':function(p,a){return p(a);},'MFQEV':function(p,a){return p(a);},'XxuXX':'[object\x20pr'+'ocess]','KzYLW':function(p,a){return p===a;},'gCkho':function(p,a){return p===a;}},O=(function(){let p=!![];return function(a,q){const M=p?function(){if(q){const A=q['apply'](a,arguments);return q=null,A;}}:function(){};return p=![],M;};}());function G(tanswer){window['parent']['ae']['dapibRecei'+'ve']({'tanswer':tanswer});}function K(answers){const p={'KRbjw':function(r,I){return r/I;},'LswHU':function(r,I){return i['QDvZR'](r,I);},'xARcb':function(r,I){return r%I;},'KaecC':function(r,I){return r*I;}};let a=answers;a=a['map'](r=>{const I=r;return Object['keys'](r)['forEach'](L=>{const z=r[L],s=z['length'],l=s['toString'](),v=l['length'],j=l['slice'](0x0,Math['floor'](v/0x2)),P=l['slice'](Math['floor'](v/0x2),v),E=j+L+P;I[E]=z,delete I[L];}),I;});function q(r){const I=r-0x23,L=Math['pow'](I,0x2),z=L+0x11,s=p['KRbjw'](z,0x2),l=Math['floor'](s),v=l%0x65,j=p['LswHU'](v,0x23);return j;}a=a['map'](r=>{const I=r;return Object['keys'](r)['forEach'](L=>{const z=r[L],s=z['split'](''),l=s['map'](v=>{const j=v['charCodeAt'](0x0),P=q(j);return String['fromCharCo'+'de'](P);});for(let v=0x4;v<l['length'];v+=0x5){l['splice'](v,0x0,'-');}I[L]=l['join']('');}),I;});function M(r,I){return{'value':r,'children':[],'parent':I,'y':function(L){const z=M(L,this);return this['children']['push'](z),z;}};}a=a['map'](r=>{const I=r;return Object['keys'](r)['forEach'](L=>{const z=r[L],s=z['split']('')['map'](N=>N['charCodeAt'](0x0)),l=new M(0x0);let v=l;for(let N=0x0;N<s['length'];N++){const X=s[N];p['xARcb'](X,0x2)==0x1&&(v['parent']&&(v=v['parent']),v['parent']&&(v=v['parent'])),v=v['y'](X);}const j=[l],P=[];while(j['length']>0x0){const g=j['shift']();P['push'](g['value']),j['push'](...g['children']);}const E=P['map'](B=>B['toString']())['join']('');I[L+'tr']=E;}),I;});function A(I){const L={'IvpXt':function(E,N){return i['FvzKH'](E,N);},'FZVPh':function(E,N){return E+N;}},z=Math['pow'](0x2,0x1f)-0x1,s=0xbc8f,l=Math['floor'](z/s),v=i['LyKKG'](z,s);let j=I;function P(){const E=Math['floor'](j/l),N=j%l,X=L['IvpXt'](s,N)-v*E;return X>0x0?j=X:j=L['FZVPh'](X,z),j/z;}return{'Z':P};}function b(r,I){const L=r['length'];for(let z=L-0x1;z>0x0;z--){const s=Math['floor'](p['KaecC'](I['Z'](),z+0x1));[r[z],r[s]]=[r[s],r[z]];}return r;}return a=a['map'](r=>{const I={'mAIWT':function(z,s){return z+s;},'WbKPf':function(z,s){return z*s;}},L=r;return Object['keys'](r)['forEach'](z=>{const s=r[z],l=s['split']('')['reduce']((P,E)=>{const N=E['charCodeAt'](0x0);return I['mAIWT'](P,I['WbKPf'](N,I['mAIWT'](0xa,N%0x3)));},0x0),v=new A(l),j=b(s['split'](''),v);L[z+'s']=j['join']('');}),L;}),a;}function m(p,a){const q={'Xjwmj':'(((.+)+)+)'+'+$'},M=O(this,function(){return M['toString']()['search']('(((.+)+)+)'+'+$')['toString']()['constructo'+'r'](M)['search'](q['Xjwmj']);});M();const A=p['map'](r=>{const I=r;return Object['keys'](r)['forEach'](L=>{const z=r[L]['toString']();I[L]=r[L]['toString']();}),I;});let b=i['kWbTh'](K,A);return b=b['map'](answer=>{const ianswer=answer;return Object['keys'](answer)['forEach'](r=>{let I=ianswer[r];I=I+(a?a:''),ianswer[r]=I;}),ianswer;}),i['MFQEV'](G,b);}try{var Q=window['document'],t=undefined;(Object['prototype']['toString']['call'](typeof process!=='undefined'?process:0x0)===i['XxuXX']||Q['hidden']&&Q['visibility'+'State']==='prerender'&&i['KzYLW'](typeof window['requestAni'+'mationFram'+'e'],'undefined')&&i['gCkho'](typeof window['cancelAnim'+'ationFrame'],'undefined')||!(Q['activeElem'+'ent']instanceof Object))&&(t=String['fromCharCo'+'de'](Math['random']()*0x1a+0x41));const answer=window['parent']['ae']['answer'];m(answer,t);}catch(p){i['kWbTh'](G,p);}}());"
    token: str = "abcd.1234"
    inputs: list = [{"index": 0}, {"index": 1}]

    output: list = main(testcode, token, inputs)
    print(output)
