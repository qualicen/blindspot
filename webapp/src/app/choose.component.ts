import { Component } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'choose',
  templateUrl: './choose.component.html',
  styleUrls: ['./choose.component.css']
})
export class ChooseComponent {
    constructor(private httpClient: HttpClient){}
    
    definition1 = null
    definition2 = null
    definition3 = null
    loading=false
    predictUrl="/api/predict"
    lookupUrl="/api/lookup"

    public search(text){
        let params=new HttpParams().set('word', text)
        this.loading=true
        forkJoin(
          this.httpClient.get(this.lookupUrl,{params}),
          this.httpClient.get(this.predictUrl,{params}),
          this.httpClient.get(this.predictUrl,{params}),
          this.httpClient.get(this.predictUrl,{params}),
        ).subscribe(([l,p1,p2,p3])=>{
          console.log(l + "\n" + p1 + "\n" + p2 + "\n" + p3)
          let defs = []
          if(l===''){
            defs.push(this.makeOption(<string>p1,false))
            defs.push(this.makeOption(<string>p2,false))
            defs.push(this.makeOption(<string>p3,false))
          } else {
            defs.push(this.makeOption(<string>l,true))
            defs.push(this.makeOption(<string>p1,false))
            if(p2===p1){
              defs.push(this.makeOption(<string>p3,false))
            } else {
              defs.push(this.makeOption(<string>p3,false))
            }
          }
          this.shuffleArray(defs)
          this.definition1=defs[0]
          this.definition2=defs[1]
          this.definition3=defs[2]
          this.loading=false
        })
    }

    private makeOption(text: string,isCorrect: boolean){
      return {
        text:text,
        isCorrect:isCorrect
      }
    }

    private shuffleArray(array) {
      for (var i = array.length - 1; i > 0; i--) {
          var j = Math.floor(Math.random() * (i + 1));
          var temp = array[i];
          array[i] = array[j];
          array[j] = temp;
      }
  }
}