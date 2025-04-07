import { Routes } from '@angular/router';
import { ProfessorListComponent } from './professor-list/professor-list.component';
import { ProfessorDetailComponent } from './professor-detail/professor-detail.component';
import { ProfessorFormComponent } from './professor-form/professor-form.component';

export const routes: Routes = [
  { path: '', redirectTo: '/list', pathMatch: 'full' },
  { path: 'list', component: ProfessorListComponent },
  { path: 'detail/:id', component: ProfessorDetailComponent },
  { path: 'form', component: ProfessorFormComponent }
];
