import { Component } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  constructor(private httpClient: HttpClient){}
  
  definition=""
  loading=false
  baseUrl="/api/predict"

  search(text){
    let params=new HttpParams().set('word', text)
    this.loading=true
    this.httpClient.get(this.baseUrl,{params}).subscribe((res:string)=>{
      console.log(res)
      this.definition=res
      this.loading=false
    })
  }

}
