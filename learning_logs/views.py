from django.http import HttpResponse

def fix_site(request):
    try:
        from django.contrib.sites.models import Site
        
        # 1. Delete any site that has this domain BUT is not ID 1 (Clears the duplicate)
        Site.objects.filter(domain='learning-log8.vercel.app').exclude(id=1).delete()
        
        # 2. Now we can safely grab or create ID 1
        site, created = Site.objects.get_or_create(id=1)
        site.domain = 'learning-log8.vercel.app'
        site.name = 'Learning Log'
        site.save()
        
        return HttpResponse("<h1>✅ SUCCESS!</h1><p>Duplicates cleared and Site 1 is perfectly fixed!</p><p><a href='/accounts/login/'>Click here to go to Login</a></p>")
    except Exception as e:
        return HttpResponse(f"<h1>❌ FAILED!</h1><p>Error details: {e}</p>")