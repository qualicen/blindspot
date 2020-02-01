import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { PredictComponent } from './predict.component';
import { HiddenIconComponent } from './hidden-icon.component'
import { ChooseComponent } from './choose.component'
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

@NgModule({
  declarations: [
    AppComponent,
    PredictComponent,
    ChooseComponent,
    HiddenIconComponent,
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    FontAwesomeModule,
    MatSlideToggleModule,
    NoopAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
