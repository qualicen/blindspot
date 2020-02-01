import { Component, Input } from '@angular/core';
import { faQuestionCircle, faCheckCircle, faTimesCircle } from '@fortawesome/free-solid-svg-icons'

@Component({
  selector: 'hidden-icon',
  templateUrl: './hidden-icon.component.html',
  styleUrls: ['./hidden-icon.component.css']
})
export class HiddenIconComponent {

    @Input()
    isCorrect:boolean

    isHidden=true
    faQuestionCircle=faQuestionCircle
    faCheckCircle=faCheckCircle
    faTimesCircle=faTimesCircle

    get icon(){
      if(this.isHidden){
        return this.faQuestionCircle
      }
      if(this.isCorrect){
        return this.faCheckCircle
      } else {
        return this.faTimesCircle
      }
    }

    public show(){
      this.isHidden=false
    }
}