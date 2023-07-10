function Create-OneWindowsAccount { 
    # Prompt for user name
    $userName = Read-Host "Enter user name"

    # Check if the user account already exists
    if (-not (Get-LocalUser -Name $userName -ErrorAction SilentlyContinue)) {
        # Prompt for password
          $password = Read-Host "Enter password for $userName" -AsSecureString
        
        # Prompt for administrator privileges
          $administrator = Read-Host "Should the user '$userName' have administrator privileges? (y/n)"
          $isAdmin = $administrator -eq 'y'

          # Create the new user account
          $userParams = @{
              'Name'         = $userName
              'Password'     = $password
              'FullName'     = $userName
              'Description'  = "User account for $userName"
              'Enabled'      = $true
              'AccountNeverExpires' = $true
              'UserMayNotChangePassword' = $false
              'PasswordNeverExpires' = $true
              'PasswordChangeNotAllowed' = $false
              'UserCannotChangePassword' = $false
              'PasswordCantChange' = $false
              'PasswordNeverExpires' = $true
              'PasswordChangeRequired' = $false
          }

          if ($isAdmin) {
              $userParams['UserFlags'] = [System.DirectoryServices.ActiveDirectoryUserAccountControl]::PasswordNotRequired -bor [System.DirectoryServices.ActiveDirectoryUserAccountControl]::DontExpirePassword
          }

          $newUser = New-LocalUser @userParams

          # Display the created user account details
          Write-Host "User account created:"
          Write-Host "Username: $($newUser.Name)"
          Write-Host "Full Name: $($newUser.FullName)"
          Write-Host "Administrator: $isAdmin"
          Write-Host "Enabled: $($newUser.Enabled)"
          Write-Host "--------"
    }
    else {
        Write-Host "User account '$userName' already exists. Please try again."
    }
}

function Create-WindowsAccounts {
    # Define the list of user names
    $userNames = @("user1", "user2", "user3")

    # Loop through the user names and create user accounts
    foreach ($userName in $userNames) {
        # Check if the user account already exists
        if (-not (Get-LocalUser -Name $userName -ErrorAction SilentlyContinue)) {
            # Prompt for password
            $password = Read-Host "Enter password for $userName" -AsSecureString

            # Prompt for administrator privileges
            $administrator = Read-Host "Should the user '$userName' have administrator privileges? (y/n)"
            $isAdmin = $administrator -eq 'y'


            # Create the new user account
            $userParams = @{
                'Name'         = $userName
                'Password'     = $password
                'FullName'     = $userName
                'Description'  = "User account for $userName"
                'Enabled'      = $true
                'AccountNeverExpires' = $true
                'UserMayNotChangePassword' = $false
                'PasswordNeverExpires' = $true
                'PasswordChangeNotAllowed' = $false
                'UserCannotChangePassword' = $false
                'PasswordCantChange' = $false
                'PasswordNeverExpires' = $true
                'PasswordChangeRequired' = $false
            }

            if ($isAdmin) {
                $userParams['UserFlags'] = [System.DirectoryServices.ActiveDirectoryUserAccountControl]::PasswordNotRequired -bor [System.DirectoryServices.ActiveDirectoryUserAccountControl]::DontExpirePassword
            }
            $newUser = New-LocalUser @userParams

            # Display the created user account details
            Write-Host "User account created:"
            Write-Host "Username: $($newUser.Name)"
            Write-Host "Full Name: $($newUser.FullName)"
            Write-Host "Administrator: $isAdmin"
            Write-Host "Enabled: $($newUser.Enabled)"
            Write-Host "--------"
        
        else {
            Write-Host "User account '$userName' already exists. Skipping..."
            Write-Host "--------"
        }
       }
    }
}

function Create-WindowsAccountsFromCSV {
    
}


function Show-Menu {
    do {
        Clear-Host
        Write-Host "=== User Account Creation ==="
        Write-Host "1. Create a Windows Account"
        Write-Host "2. Create multiple Windows Accounts"
        Write-Host "3. Exit"
        $choice = Read-Host "Enter your choice"
    
        switch ($choice) {
            "1" {
                Create-OneWindowsAccount
                Pause
            }
            "2" {
                Create-WindowsAccounts
                Pause
            }
            "3" {
                break
            }
            default {
                Write-Host "Invalid choice. Please try again."
                Pause
            }
        }
    } while ($choice -ne "2")
}

Show-Menu