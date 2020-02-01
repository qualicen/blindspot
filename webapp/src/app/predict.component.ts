
import { Component } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Component({
  selector: 'predict',
  templateUrl: './predict.component.html',
  styleUrls: ['./predict.component.css']
})
export class PredictComponent {
    constructor(private httpClient: HttpClient){}
    
    definition=""
    loading=false
    baseUrl="/api/predict"

    public search(text){
        let params=new HttpParams().set('word', text)
        this.loading=true
        this.httpClient.get(this.baseUrl,{params}).subscribe((res:string)=>{
        console.log(res)
        this.definition=res
        this.loading=false
        })
    }
}