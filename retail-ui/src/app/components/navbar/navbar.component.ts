import { Component, Input } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable, timer } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { UserService } from 'src/app/services/user.service';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { LoginComponent } from '../login/login.component';
import { User } from 'src/app/models/user.model';
import { SpinnereventsService } from 'src/app/services/spinnerevents.service';

@Component({
  selector: 'navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {
  isLoggedIn: boolean = false;
  spinner: boolean = false;

  @Input() itemsInCart = 0;

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
  );

  ngOnInit(): void {
    // get new JWT token every 5 min.
    timer(0, 300000).subscribe(()=>{
      this.userService.refreshJwtToken().subscribe({
        next: (response) => {
          console.log("got it");
        },
        error: (error) => {
          console.log("error");
        }
      })
    });

    // subscribe for login event
    this.userService.loginEvent.subscribe({
      next: (response: User) => {
        this.isLoggedIn = true;
        console.log(response);
      }
    });

    // subscribe for logout event
    this.userService.logoutEvent.subscribe({
      next: (response: any) => {
        this.isLoggedIn = false;
        console.log(response);
      }
    });

    // subscribe for spinner event
    this.spinnerEvents.spinnerEvent.subscribe({
      next: (response: boolean) => {
        this.spinner = response;
      }
    });

    // Check if user is logged in or not
    this.checkIsLoggedIn();
  }

  constructor(private breakpointObserver: BreakpointObserver, private userService: UserService, public dialog: MatDialog, private spinnerEvents: SpinnereventsService) {}

  checkIsLoggedIn(){
    this.userService.getLoggedInUserProfile().subscribe({
      next: (response) => {
        this.isLoggedIn = true;
      },
      error: (error) => {
        this.isLoggedIn = false;
      }
    });
  }

  openDialog(enterAnimationDuration: string, exitAnimationDuration: string): void {
    
    this.dialog.open(LoginComponent, {
      width: '350px',
      enterAnimationDuration,
      exitAnimationDuration,
    });
  }

  doLogout() {
    this.spinnerEvents.spinnerEvent.emit(true);
    this.userService.doLogoutFromApp().subscribe({
      next: (response) => {
        this.userService.logoutEvent.emit(null);
        this.spinnerEvents.spinnerEvent.emit(false);
      },
      error: (error) => {
        console.log(error);
        this.spinnerEvents.spinnerEvent.emit(false);
      }
    });
  }

}
