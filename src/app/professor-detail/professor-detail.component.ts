import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { ProfessorService, Professor } from '../professor.service';

@Component({
  selector: 'app-professor-detail',
  standalone: true,
  imports: [CommonModule, RouterModule, MatCardModule, MatButtonModule],
  templateUrl: './professor-detail.component.html',
  styleUrls: ['./professor-detail.component.css']
})
export class ProfessorDetailComponent implements OnInit {
  professor: Professor | undefined;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private professorService: ProfessorService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.professorService.getProfessor(id).subscribe({
      next: data => this.professor = data,
      error: err => console.error('Error fetching professor:', err)
    });
  }

  deleteProfessor(): void {
    if (this.professor) {
      this.professorService.deleteProfessor(this.professor.id).subscribe({
        next: () => this.router.navigate(['/list']),
        error: err => console.error('Error deleting professor:', err)
      });
    }
  }
}
