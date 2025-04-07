import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { Professor, ProfessorService } from '../professor.service';

@Component({
  selector: 'app-professor-form',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './professor-form.component.html',
  styleUrls: ['./professor-form.component.css']
})
export class ProfessorFormComponent {
  professor: Professor = {
    id: 0,
    name: '',
    title: '',
    department: ''
  };

  constructor(private professorService: ProfessorService, private router: Router) {}

  onSubmit(): void {
    console.log("Form submitted", this.professor);
    this.professorService.addProfessor(this.professor).subscribe({
      next: () => this.router.navigate(['/list']),
      error: err => console.error('Error adding professor:', err)
    });
  }
}
