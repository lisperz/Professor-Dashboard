import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { ProfessorService, Professor } from '../professor.service';

@Component({
  selector: 'app-professor-list',
  standalone: true,
  imports: [CommonModule, RouterModule, MatCardModule, MatButtonModule],
  templateUrl: './professor-list.component.html',
  styleUrls: ['./professor-list.component.css']
})
export class ProfessorListComponent implements OnInit {
  professors: Professor[] = [];

  constructor(private professorService: ProfessorService) {}

  ngOnInit(): void {
    this.professorService.getProfessors().subscribe({
      next: data => this.professors = data,
      error: err => console.error('Error fetching professors:', err)
    });
  }
}
